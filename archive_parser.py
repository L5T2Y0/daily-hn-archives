# Archive Parser 模块 - 统一处理归档文件解析
from pathlib import Path
import re


def parse_archive_file(file_path: Path) -> list[dict]:
    """
    解析归档文件，提取文章信息

    参数:
        file_path: 归档文件路径

    返回:
        文章列表，每篇文章包含 title, url, score, comments, date
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        articles = []

        # 从文件名提取日期
        date_str = file_path.stem  # 例如: 2026-02-14

        # 匹配格式: 1. [title](url) - score points, comments comments
        pattern = r"\d+\.\s+\[(.+?)\]\((.+?)\)\s+-\s+(\d+)\s+points,\s+(\d+)\s+comments"
        matches = re.findall(pattern, content)

        for title, url, score, comments in matches:
            articles.append(
                {"title": title, "url": url, "score": int(score), "comments": int(comments), "date": date_str}
            )

        return articles
    except Exception:
        return []
