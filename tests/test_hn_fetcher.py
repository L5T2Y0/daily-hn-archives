"""
测试 hn_fetcher 模块
"""
import pytest
from unittest.mock import Mock, patch
from hn_fetcher import (
    validate_story_data,
    HNAPIError,
    HNTimeoutError,
    HNConnectionError,
    HNDataError,
)


class TestValidateStoryData:
    """测试数据验证函数"""
    
    def test_valid_story_data(self):
        """测试有效的文章数据"""
        data = {
            "title": "Test Article",
            "score": 100,
            "descendants": 50
        }
        assert validate_story_data(data) is True
    
    def test_missing_title(self):
        """测试缺少标题"""
        data = {"score": 100}
        assert validate_story_data(data) is False
    
    def test_empty_title(self):
        """测试空标题"""
        data = {"title": "", "score": 100}
        assert validate_story_data(data) is False
    
    def test_missing_score(self):
        """测试缺少分数"""
        data = {"title": "Test"}
        assert validate_story_data(data) is False
    
    def test_invalid_score_type(self):
        """测试无效的分数类型"""
        data = {"title": "Test", "score": "100"}
        assert validate_story_data(data) is False
    
    def test_none_descendants(self):
        """测试评论数为None"""
        data = {"title": "Test", "score": 100, "descendants": None}
        assert validate_story_data(data) is True
    
    def test_invalid_descendants_type(self):
        """测试无效的评论数类型"""
        data = {"title": "Test", "score": 100, "descendants": "50"}
        assert validate_story_data(data) is False


class TestFetchWithRetry:
    """测试重试机制"""
    
    @patch('hn_fetcher.requests.get')
    def test_successful_request(self, mock_get):
        """测试成功的请求"""
        from hn_fetcher import fetch_with_retry
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        result = fetch_with_retry("http://test.com")
        assert result == {"test": "data"}
        assert mock_get.call_count == 1
    
    @patch('hn_fetcher.requests.get')
    @patch('hn_fetcher.time.sleep')
    def test_retry_on_timeout(self, mock_sleep, mock_get):
        """测试超时重试"""
        from hn_fetcher import fetch_with_retry
        import requests
        
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(HNTimeoutError):
            fetch_with_retry("http://test.com", max_retries=3)
        
        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2  # 最后一次不sleep
    
    @patch('hn_fetcher.requests.get')
    def test_rate_limit_error(self, mock_get):
        """测试速率限制"""
        from hn_fetcher import fetch_with_retry
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        with pytest.raises(HNAPIError):
            fetch_with_retry("http://test.com")


class TestGetTopStoryIds:
    """测试获取文章ID列表"""
    
    @patch('hn_fetcher.fetch_with_retry')
    def test_valid_story_ids(self, mock_fetch):
        """测试有效的ID列表"""
        from hn_fetcher import get_top_story_ids
        
        mock_fetch.return_value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        result = get_top_story_ids(5)
        assert result == [1, 2, 3, 4, 5]
    
    @patch('hn_fetcher.fetch_with_retry')
    def test_empty_list(self, mock_fetch):
        """测试空列表"""
        from hn_fetcher import get_top_story_ids
        
        mock_fetch.return_value = []
        
        with pytest.raises(HNDataError):
            get_top_story_ids(10)
    
    @patch('hn_fetcher.fetch_with_retry')
    def test_invalid_data_type(self, mock_fetch):
        """测试无效的数据类型"""
        from hn_fetcher import get_top_story_ids
        
        mock_fetch.return_value = {"not": "a list"}
        
        with pytest.raises(HNDataError):
            get_top_story_ids(10)
