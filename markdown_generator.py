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
    lines = []
    
    # 项目说明
    lines.append("# Daily Hacker News Archives")
    lines.append("")
    lines.append("每天自动获取并归档 Hacker News 的 Top 10 热门文章。")
    lines.append("")
    
    # 最后更新时间
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"*最后更新: {timestamp}*")
    lines.append("")
    
    # 今日 Top 10
    lines.append("## 今日 Top 10")
    lines.append("")
    for i, story in enumerate(today_stories, 1):
        lines.append(format_story(i, story))
    lines.append("")
    
    # 历史归档
    lines.append("## 历史归档")
    lines.append("")
    for archive_file in archive_files:
        # 提取日期（去掉 .md 扩展名）
        date = archive_file.replace(".md", "")
        lines.append(f"- [{date}](archives/{archive_file})")
    lines.append("")
    
    # 页脚
    lines.append("---")
    lines.append("*由 [Daily HN Archives](https://github.com/HackerNews/API) 自动生成*")
    
    return "\n".join(lines)
