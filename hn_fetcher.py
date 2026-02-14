# HN Fetcher 模块 - 负责与 Hacker News API 交互
"""
Hacker News API 交互模块
提供获取热门文章的功能，包含自动重试机制
"""
import requests
import time
from typing import List, Dict


# API 端点常量
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{HN_API_BASE}/topstories.json"
ITEM_URL_TEMPLATE = f"{HN_API_BASE}/item/{{id}}.json"


def fetch_with_retry(url: str, max_retries: int = 3, delay: int = 2) -> dict:
    """
    发送 HTTP GET 请求并实现重试机制
    
    参数:
        url: 请求的 URL
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    
    返回:
        解析后的 JSON 响应（字典）
    
    异常:
        如果所有重试都失败，抛出 Exception
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"  请求失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                time.sleep(delay)
            else:
                raise Exception(f"请求失败，已重试 {max_retries} 次: {e}")


def get_top_story_ids(limit: int = 10) -> List[int]:
    """
    获取 Top Stories 的 ID 列表
    
    参数:
        limit: 获取的文章数量
    
    返回:
        文章 ID 列表
    """
    try:
        data = fetch_with_retry(TOP_STORIES_URL)
        if not data:
            raise Exception("Top Stories 返回空列表")
        return data[:limit]
    except Exception as e:
        print(f"获取 Top Stories 失败: {e}")
        raise


def get_story_details(story_id: int) -> Dict[str, any]:
    """
    获取单篇文章的详细信息
    
    参数:
        story_id: 文章 ID
    
    返回:
        包含 title, url, score, comments 的字典
        如果文章没有 url，使用 HN 讨论页链接
    """
    url = ITEM_URL_TEMPLATE.format(id=story_id)
    try:
        data = fetch_with_retry(url)
        
        # 提取必需字段
        title = data.get("title", "无标题")
        score = data.get("score", 0)
        comments = data.get("descendants", 0)
        
        # 如果没有 url，使用 HN 讨论页链接
        story_url = data.get("url")
        if not story_url:
            story_url = f"https://news.ycombinator.com/item?id={story_id}"
        
        return {
            "title": title,
            "url": story_url,
            "score": score,
            "comments": comments
        }
    except Exception as e:
        print(f"  获取文章 {story_id} 详情失败: {e}")
        raise


def fetch_top_stories(count: int = 10) -> List[Dict[str, any]]:
    """
    获取 Top N 篇文章的完整信息
    
    参数:
        count: 获取的文章数量
    
    返回:
        文章详情列表
    """
    print(f"正在获取 Top {count} 文章...")
    story_ids = get_top_story_ids(count)
    stories = []
    
    for idx, story_id in enumerate(story_ids, 1):
        try:
            story = get_story_details(story_id)
            stories.append(story)
            print(f"  [{idx}/{count}] ✓ {story['title'][:50]}...")
        except Exception as e:
            print(f"  [{idx}/{count}] ✗ 跳过文章 {story_id}")
            continue
    
    return stories
