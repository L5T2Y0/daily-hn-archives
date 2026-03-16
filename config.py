"""
配置文件 - 集中管理项目配置
支持环境变量覆盖默认配置
"""

import os

# API 配置
HN_API_BASE = os.getenv("HN_API_BASE", "https://hacker-news.firebaseio.com/v0")
TOP_STORIES_ENDPOINT = f"{HN_API_BASE}/topstories.json"
ITEM_ENDPOINT_TEMPLATE = f"{HN_API_BASE}/item/{{id}}.json"

# 请求配置
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))

# 文章获取配置
ARTICLE_COUNT = int(os.getenv("ARTICLE_COUNT", "10"))
WEEKLY_TOP_COUNT = int(os.getenv("WEEKLY_TOP_COUNT", "20"))
MONTHLY_TOP_COUNT = int(os.getenv("MONTHLY_TOP_COUNT", "50"))

# 文件路径配置
ARCHIVES_DIR = os.getenv("ARCHIVES_DIR", "archives")
WEEKLY_DIR = os.getenv("WEEKLY_DIR", "weekly")
MONTHLY_DIR = os.getenv("MONTHLY_DIR", "monthly")
README_FILE = os.getenv("README_FILE", "README.md")

# 时区配置
TIMEZONE_OFFSET = int(os.getenv("TIMEZONE_OFFSET", "8"))  # 北京时间 UTC+8

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
