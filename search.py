# Search 模块 - 负责搜索历史文章
from datetime import datetime
from pathlib import Path
import re
from typing import Optional
from tag_classifier import add_tags_to_article, format_tags_for_display


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
        pattern = r'\d+\.\s+\[(.+?)\]\((.+?)\)\s+-\s+(\d+)\s+points,\s+(\d+)\s+comments'
        matches = re.findall(pattern, content)
        
        for title, url, score, comments in matches:
            articles.append({
                "title": title,
                "url": url,
                "score": int(score),
                "comments": int(comments),
                "date": date_str
            })
        
        return articles
    except Exception:
        return []


def load_all_articles() -> list[dict]:
    """
    加载所有归档文章
    
    返回:
        所有文章列表
    """
    archives_dir = Path("archives")
    all_articles = []
    
    if not archives_dir.exists():
        return all_articles
    
    # 遍历所有归档文件
    for file_path in sorted(archives_dir.glob("*.md")):
        if file_path.name == ".gitkeep":
            continue
        articles = parse_archive_file(file_path)
        all_articles.extend(articles)
    
    return all_articles


def search_articles(
    query: str,
    articles: Optional[list[dict]] = None,
    limit: int = 20,
    sort_by: str = "relevance"
) -> list[dict]:
    """
    搜索文章
    
    参数:
        query: 搜索关键词
        articles: 文章列表（如果为None则加载所有文章）
        limit: 返回结果数量限制
        sort_by: 排序方式 ("relevance" 相关度, "score" 分数, "date" 日期, "comments" 评论数)
    
    返回:
        匹配的文章列表
    """
    if articles is None:
        articles = load_all_articles()
    
    if not query:
        return []
    
    query_lower = query.lower()
    query_words = query_lower.split()
    
    results = []
    
    for article in articles:
        title_lower = article["title"].lower()
        url_lower = article["url"].lower()
        
        # 计算相关度分数
        relevance_score = 0
        
        # 完整匹配（最高权重）
        if query_lower in title_lower:
            relevance_score += 100
        
        # 单词匹配
        for word in query_words:
            if word in title_lower:
                relevance_score += 10
            if word in url_lower:
                relevance_score += 5
        
        # 如果有匹配，添加到结果
        if relevance_score > 0:
            article_copy = article.copy()
            article_copy["relevance_score"] = relevance_score
            results.append(article_copy)
    
    # 排序
    if sort_by == "relevance":
        results.sort(key=lambda x: (x["relevance_score"], x["score"]), reverse=True)
    elif sort_by == "score":
        results.sort(key=lambda x: x["score"], reverse=True)
    elif sort_by == "date":
        results.sort(key=lambda x: x["date"], reverse=True)
    elif sort_by == "comments":
        results.sort(key=lambda x: x["comments"], reverse=True)
    
    return results[:limit]


def search_by_tag(tag: str, articles: Optional[list[dict]] = None, limit: int = 20) -> list[dict]:
    """
    按标签搜索文章
    
    参数:
        tag: 标签名称
        articles: 文章列表（如果为None则加载所有文章）
        limit: 返回结果数量限制
    
    返回:
        匹配的文章列表
    """
    if articles is None:
        articles = load_all_articles()
    
    # 为所有文章添加标签
    for article in articles:
        if "tags" not in article:
            add_tags_to_article(article)
    
    # 筛选包含指定标签的文章
    results = [article for article in articles if tag in article.get("tags", [])]
    
    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:limit]


def format_search_results(results: list[dict], show_tags: bool = True) -> str:
    """
    格式化搜索结果为Markdown
    
    参数:
        results: 搜索结果列表
        show_tags: 是否显示标签
    
    返回:
        Markdown格式的搜索结果
    """
    if not results:
        return "未找到匹配的文章。"
    
    lines = []
    lines.append(f"找到 {len(results)} 篇相关文章：")
    lines.append("")
    
    for i, article in enumerate(results, 1):
        title = article["title"]
        url = article["url"]
        score = article["score"]
        comments = article["comments"]
        date = article["date"]
        
        lines.append(f"{i}. [{title}]({url})")
        lines.append(f"   - ⭐ {score} points | 💬 {comments} comments | 📅 {date}")
        
        if show_tags and "tags" in article:
            tags = format_tags_for_display(article["tags"])
            if tags:
                lines.append(f"   - {tags}")
        
        lines.append("")
    
    return "\n".join(lines)


def interactive_search():
    """
    交互式搜索命令行界面
    """
    print("=" * 60)
    print("Hacker News Archives - 文章搜索")
    print("=" * 60)
    print()
    
    # 加载所有文章
    print("正在加载文章...")
    articles = load_all_articles()
    print(f"已加载 {len(articles)} 篇文章")
    print()
    
    # 为所有文章添加标签
    print("正在分析标签...")
    for article in articles:
        add_tags_to_article(article)
    print("标签分析完成")
    print()
    
    while True:
        print("-" * 60)
        print("搜索选项：")
        print("1. 关键词搜索")
        print("2. 标签搜索")
        print("3. 退出")
        print()
        
        choice = input("请选择 (1-3): ").strip()
        print()
        
        if choice == "1":
            query = input("请输入搜索关键词: ").strip()
            if not query:
                print("搜索关键词不能为空")
                continue
            
            print()
            print("排序方式：")
            print("1. 相关度 (默认)")
            print("2. 分数")
            print("3. 日期")
            print("4. 评论数")
            sort_choice = input("请选择排序方式 (1-4, 默认1): ").strip() or "1"
            
            sort_map = {
                "1": "relevance",
                "2": "score",
                "3": "date",
                "4": "comments"
            }
            sort_by = sort_map.get(sort_choice, "relevance")
            
            print()
            print(f"搜索关键词: {query}")
            print(f"排序方式: {sort_by}")
            print()
            
            results = search_articles(query, articles, limit=20, sort_by=sort_by)
            print(format_search_results(results))
            
        elif choice == "2":
            print("可用标签：")
            print("AI, Web, DevOps, Database, Security, Programming,")
            print("Mobile, Startup, Open Source, Performance, Tools, Science")
            print()
            
            tag = input("请输入标签名称: ").strip()
            if not tag:
                print("标签名称不能为空")
                continue
            
            print()
            print(f"搜索标签: {tag}")
            print()
            
            results = search_by_tag(tag, articles, limit=20)
            print(format_search_results(results))
            
        elif choice == "3":
            print("感谢使用！")
            break
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    interactive_search()
