"""
工具函数模块
提供通用的辅助函数
"""

import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from config import TIMEZONE_OFFSET, LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    设置日志记录器

    参数:
        name: 日志记录器名称
        level: 日志级别（可选，默认使用配置）

    返回:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # 设置日志级别
        log_level = level or LOG_LEVEL
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger.level)

        # 设置格式
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


def get_beijing_time() -> datetime:
    """
    获取北京时间

    返回:
        北京时间的datetime对象
    """
    beijing_tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    return datetime.now(beijing_tz)


def format_beijing_time(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化北京时间

    参数:
        dt: datetime对象（可选，默认当前时间）
        fmt: 时间格式字符串

    返回:
        格式化的时间字符串
    """
    if dt is None:
        dt = get_beijing_time()
    return dt.strftime(fmt)


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，不存在则创建

    参数:
        path: 目录路径

    返回:
        Path对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def safe_read_file(path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    安全读取文件

    参数:
        path: 文件路径
        encoding: 文件编码

    返回:
        文件内容，失败返回None
    """
    try:
        return Path(path).read_text(encoding=encoding)
    except (OSError, IOError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to read file {path}: {e}")
        return None


def safe_write_file(path: str, content: str, encoding: str = "utf-8") -> bool:
    """
    安全写入文件

    参数:
        path: 文件路径
        content: 文件内容
        encoding: 文件编码

    返回:
        是否成功
    """
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return True
    except (OSError, IOError) as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to write file {path}: {e}")
        return False


def validate_date_string(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    """
    验证日期字符串格式

    参数:
        date_str: 日期字符串
        fmt: 日期格式

    返回:
        是否有效
    """
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False
