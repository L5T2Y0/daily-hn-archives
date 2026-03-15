"""
测试 utils 模块
"""
import pytest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from utils import (
    get_beijing_time,
    format_beijing_time,
    validate_date_string,
    ensure_dir,
)


class TestBeijingTime:
    """测试北京时间相关函数"""
    
    def test_get_beijing_time(self):
        """测试获取北京时间"""
        beijing_time = get_beijing_time()
        assert isinstance(beijing_time, datetime)
        # 验证时区偏移
        assert beijing_time.utcoffset() == timedelta(hours=8)
    
    def test_format_beijing_time(self):
        """测试格式化北京时间"""
        result = format_beijing_time()
        # 验证格式
        assert len(result) == 19  # YYYY-MM-DD HH:MM:SS
        assert result[4] == '-'
        assert result[7] == '-'
        assert result[10] == ' '
        assert result[13] == ':'
        assert result[16] == ':'
    
    def test_format_beijing_time_custom_format(self):
        """测试自定义格式"""
        result = format_beijing_time(fmt="%Y-%m-%d")
        assert len(result) == 10
        assert result[4] == '-'
        assert result[7] == '-'


class TestValidateDateString:
    """测试日期验证"""
    
    def test_valid_date(self):
        """测试有效日期"""
        assert validate_date_string("2026-02-24") is True
    
    def test_invalid_date_format(self):
        """测试无效格式"""
        assert validate_date_string("24-02-2026") is False
    
    def test_invalid_date_value(self):
        """测试无效日期值"""
        assert validate_date_string("2026-13-01") is False
    
    def test_custom_format(self):
        """测试自定义格式"""
        assert validate_date_string("24/02/2026", fmt="%d/%m/%Y") is True


class TestEnsureDir:
    """测试目录创建"""
    
    def test_ensure_dir_creates_directory(self, tmp_path):
        """测试创建目录"""
        test_dir = tmp_path / "test_dir"
        result = ensure_dir(str(test_dir))
        
        assert result.exists()
        assert result.is_dir()
    
    def test_ensure_dir_existing_directory(self, tmp_path):
        """测试已存在的目录"""
        test_dir = tmp_path / "existing_dir"
        test_dir.mkdir()
        
        result = ensure_dir(str(test_dir))
        assert result.exists()
        assert result.is_dir()
