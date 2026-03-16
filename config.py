"""
配置文件 - 集中管理项目配置
支持环境变量覆盖默认配置
"""
import os


def _get_int_in_range(env_var: str, default: int, min_val: int, max_val: int) -> int:
    """读取环境变量为整数并验证范围，无效时回退到默认值"""
    raw = os.getenv(env_var, str(default))
    try:
        value = int(raw)
        if not (min_val <= value <= max_val):
            raise ValueError(f"{env_var} must be between {min_val} and {max_val}, got {value}")
        return value
    except ValueError as e:
        import warnings
        warnings.warn(
            f"Invalid value for {env_var}={raw!r}: {e}. Using default {default}."
        )
        return default


# API 配置
HN_API_BASE = os.getenv("HN_API_BASE", "https://hacker-news.firebaseio.com/v0")
TOP_STORIES_ENDPOINT = f"{HN_API_BASE}/topstories.json"
ITEM_ENDPOINT_TEMPLATE = f"{HN_API_BASE}/item/{{id}}.json"

# 请求配置
REQUEST_TIMEOUT = _get_int_in_range("REQUEST_TIMEOUT", 10, 1, 300)
MAX_RETRIES = _get_int_in_range("MAX_RETRIES", 3, 1, 10)
RETRY_DELAY = _get_int_in_range("RETRY_DELAY", 2, 1, 60)

# 文章获取配置
ARTICLE_COUNT = _get_int_in_range("ARTICLE_COUNT", 10, 1, 500)
WEEKLY_TOP_COUNT = _get_int_in_range("WEEKLY_TOP_COUNT", 20, 1, 500)
MONTHLY_TOP_COUNT = _get_int_in_range("MONTHLY_TOP_COUNT", 50, 1, 500)

# 文件路径配置
ARCHIVES_DIR = os.getenv("ARCHIVES_DIR", "archives")
WEEKLY_DIR = os.getenv("WEEKLY_DIR", "weekly")
MONTHLY_DIR = os.getenv("MONTHLY_DIR", "monthly")
README_FILE = os.getenv("README_FILE", "README.md")

# 时区配置（有效 UTC 偏移范围：-12 到 +14）
TIMEZONE_OFFSET = _get_int_in_range("TIMEZONE_OFFSET", 8, -12, 14)  # 默认北京时间 UTC+8

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
