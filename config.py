"""
配置文件 - 集中管理项目配置
"""

# 文章获取配置
ARTICLE_COUNT = 10  # 每天获取的文章数量
MAX_RETRIES = 3  # API 请求最大重试次数
RETRY_DELAY = 2  # 重试间隔（秒）
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）

# 文件路径配置
ARCHIVES_DIR = "archives"  # 归档文件目录
README_FILE = "README.md"  # README 文件名

# API 端点配置
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_ENDPOINT = f"{HN_API_BASE}/topstories.json"
ITEM_ENDPOINT_TEMPLATE = f"{HN_API_BASE}/item/{{id}}.json"

# 时区配置
TIMEZONE_OFFSET = 8  # 北京时间 UTC+8
