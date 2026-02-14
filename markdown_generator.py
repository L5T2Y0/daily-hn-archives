# Markdown Generator 模块 - 负责生成 Markdown 内容
from datetime import datetime


def format_story(index: int, story: dict) -> str:
    """
    将单篇文章格式化为 Markdown 列表项
    
    参数:
        index: 文章序号（1-10）
        story: 文章详情字典
    
    返回:
        格式化的 Markdown 字符串
        格式: "{index}. [{title}]({url}) - {score} points, {comments} comments"
    """
    title = story["title"]
    url = story["url"]
    score = story["score"]
    comments = story["comments"]
    
    return f"{index}. [{title}]({url}) - {score} points, {comments} comments"


def generate_archive_content(stories: list[dict], date: str) -> str:
    """
    生成完整的归档文件内容
    
    参数:
        stories: 文章列表
        date: 日期字符串（YYYY-MM-DD）
    
    返回:
        完整的 Markdown 内容，包含标题、文章列表和页脚
    """
    lines = []
    
    # 添加标题
    lines.append(f"# Hacker News Top 10 - {date}")
    lines.append("")
    
    # 添加文章列表
    for i, story in enumerate(stories, 1):
        lines.append(format_story(i, story))
    
    # 添加页脚
    lines.append("")
    lines.append("---")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"*归档生成时间: {timestamp}*")
    lines.append("*数据来源: [Hacker News API](https://github.com/HackerNews/API)*")
    
    return "\n".join(lines)


def generate_readme_content(today_stories: list[dict], archive_files: list[str]) -> str:
    """
    生成 README.md 的完整内容
    
    参数:
        today_stories: 今日文章列表
        archive_files: 归档文件名列表（按日期倒序）
    
    返回:
        完整的 README Markdown 内容
    """
    # 读取现有的 README 模板
    try:
        from pathlib import Path
        readme_path = Path("README.md")
        if readme_path.exists():
            readme_template = readme_path.read_text(encoding="utf-8")
        else:
            # 如果 README 不存在，使用简单模板
            readme_template = """# Daily Hacker News Archives

每天自动获取并归档 Hacker News 的 Top 10 热门文章。

<!-- DAILY_ARTICLES_START -->
<!-- DAILY_ARTICLES_END -->

## 历史归档

"""
    except Exception:
        readme_template = """# Daily Hacker News Archives

每天自动获取并归档 Hacker News 的 Top 10 热门文章。

<!-- DAILY_ARTICLES_START -->
<!-- DAILY_ARTICLES_END -->

## 历史归档

"""
    
    # 生成今日文章内容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    articles_content = f"> 最后更新：{timestamp}\n\n"
    
    for i, story in enumerate(today_stories, 1):
        articles_content += format_story(i, story) + "\n"
    
    articles_content += f"\n📁 **[查看所有历史归档](archives/)** | 共 {len(archive_files)} 个归档文件\n"
    
    # 替换每日文章区域
    import re
    pattern = r'<!-- DAILY_ARTICLES_START -->.*?<!-- DAILY_ARTICLES_END -->'
    replacement = f'<!-- DAILY_ARTICLES_START -->\n{articles_content}\n<!-- DAILY_ARTICLES_END -->'
    
    updated_readme = re.sub(pattern, replacement, readme_template, flags=re.DOTALL)
    
    return updated_readme
