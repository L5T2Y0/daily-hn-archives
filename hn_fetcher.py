# HN Fetcher 模块 - 负责与 Hacker News API 交互
"""
Hacker News API 交互模块
提供获取热门文章的功能，包含完善的错误处理和重试机制
"""
import requests
import time
from typing import List, Dict, Optional


# API 端点常量
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{HN_API_BASE}/topstories.json"
ITEM_URL_TEMPLATE = f"{HN_API_BASE}/item/{{id}}.json"


# 自定义异常类
class HNAPIError(Exception):
    """Hacker News API 基础异常"""
    pass


class HNRateLimitError(HNAPIError):
    """API 速率限制异常"""
    pass


class HNConnectionError(HNAPIError):
    """API 连接异常"""
    pass


class HNTimeoutError(HNAPIError):
    """API 超时异常"""
    pass


class HNDataError(HNAPIError):
    """API 数据格式异常"""
    pass


def fetch_with_retry(url: str, max_retries: int = 3, timeout: int = 10) -> dict:
    """
    带指数退避的重试请求
    
    参数:
        url: 请求URL
        max_retries: 最大重试次数
        timeout: 超时时间（秒）
    
    返回:
        JSON响应数据
    
    异常:
        HNTimeoutError: 请求超时
        HNConnectionError: 连接失败
        HNRateLimitError: 速率限制
        HNAPIError: 其他API错误
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            
            # 检查速率限制
            if response.status_code == 429:
                raise HNRateLimitError(f"API rate limit exceeded: {url}")
            
            # 检查其他HTTP错误
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout as e:
            if attempt == max_retries - 1:
                raise HNTimeoutError(f"Request timeout after {max_retries} attempts: {url}") from e
            # 指数退避
            wait_time = 2 ** attempt
            print(f"  ⚠️  Timeout, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            
        except requests.exceptions.ConnectionError as e:
            if attempt == max_retries - 1:
                raise HNConnectionError(f"Connection failed after {max_retries} attempts: {url}") from e
            wait_time = 2 ** attempt
            print(f"  ⚠️  Connection error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
            
        except requests.exceptions.HTTPError as e:
            # HTTP错误不重试（除了429已经处理）
            raise HNAPIError(f"HTTP error {response.status_code}: {url}") from e
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise HNAPIError(f"Request failed after {max_retries} attempts: {url}") from e
            wait_time = 2 ** attempt
            print(f"  ⚠️  Request error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    
    raise HNAPIError(f"Failed to fetch {url} after {max_retries} attempts")


def validate_story_data(data: dict) -> bool:
    """
    验证文章数据格式
    
    参数:
        data: API返回的文章数据
    
    返回:
        是否有效
    """
    if not isinstance(data, dict):
        return False
    
    # title 必须存在且为字符串
    if "title" not in data or not isinstance(data["title"], str) or not data["title"].strip():
        return False
    
    # score 必须存在且为数字
    if "score" not in data or not isinstance(data["score"], (int, float)):
        return False
    
    # descendants (评论数) 必须是数字或None
    if "descendants" in data and data["descendants"] is not None:
        if not isinstance(data["descendants"], (int, float)):
            return False
    
    return True


def get_top_story_ids(limit: int = 10) -> List[int]:
    """
    获取 Top Stories 的 ID 列表
    
    参数:
        limit: 获取的文章数量
    
    返回:
        文章 ID 列表
    
    异常:
        HNDataError: 数据格式错误
        HNAPIError: API请求失败
    """
    try:
        data = fetch_with_retry(TOP_STORIES_URL)
        
        # 验证数据格式
        if not isinstance(data, list):
            raise HNDataError(f"Expected list, got {type(data)}")
        
        if not data:
            raise HNDataError("Top Stories returned empty list")
        
        # 验证ID都是整数
        story_ids = data[:limit]
        if not all(isinstance(id, int) for id in story_ids):
            raise HNDataError("Story IDs must be integers")
        
        return story_ids
        
    except HNAPIError:
        raise
    except Exception as e:
        raise HNDataError(f"Failed to parse Top Stories data: {e}") from e


def get_story_details(story_id: int) -> Optional[Dict[str, any]]:
    """
    获取单篇文章的详细信息
    
    参数:
        story_id: 文章 ID
    
    返回:
        包含 title, url, score, comments 的字典
        如果文章无效或获取失败，返回 None
    """
    url = ITEM_URL_TEMPLATE.format(id=story_id)
    
    try:
        data = fetch_with_retry(url)
        
        # 验证数据格式
        if not validate_story_data(data):
            print(f"  ⚠️  Invalid data format for story {story_id}")
            return None
        
        # 提取字段
        title = data["title"].strip()
        score = int(data["score"])
        comments = int(data.get("descendants", 0))
        
        # 如果没有 url，使用 HN 讨论页链接
        story_url = data.get("url", "").strip()
        if not story_url:
            story_url = f"https://news.ycombinator.com/item?id={story_id}"
        
        return {
            "title": title,
            "url": story_url,
            "score": score,
            "comments": comments
        }
        
    except (HNAPIError, HNDataError) as e:
        print(f"  ⚠️  Failed to fetch story {story_id}: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Unexpected error for story {story_id}: {e}")
        return None


def fetch_top_stories(count: int = 10) -> List[Dict[str, any]]:
    """
    获取 Top N 篇文章的完整信息
    
    参数:
        count: 获取的文章数量
    
    返回:
        文章详情列表（跳过失败的文章）
    
    异常:
        HNAPIError: 无法获取文章ID列表
    """
    print(f"正在获取 Top {count} 文章...")
    
    try:
        story_ids = get_top_story_ids(count)
    except HNAPIError as e:
        print(f"❌ 无法获取文章列表: {e}")
        raise
    
    stories = []
    
    for idx, story_id in enumerate(story_ids, 1):
        story = get_story_details(story_id)
        if story:
            stories.append(story)
            print(f"  [{idx}/{count}] ✓ {story['title'][:50]}...")
        else:
            print(f"  [{idx}/{count}] ✗ 跳过文章 {story_id}")
    
    if not stories:
        raise HNDataError("No valid stories fetched")
    
    print(f"成功获取 {len(stories)} 篇文章")
    return stories
