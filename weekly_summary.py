# Weekly Summary 模块 - 负责生成周报
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from tag_classifier import add_tags_to_article, group_articles_by_tag, get_tag_statistics, format_tags_for_display


def get_week_date_range() -> tuple[str, str]:
    """
    获取上周的日期范围（周一到周日）
    
    返回:
        (start_date, end_date) 格式为 YYYY-MM-DD
    """
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).date()
    
    # 计算上周一和上周日
    weekday = today.weekday()  # 0=周一, 6=周日
    last_sunday = today - timedelta(days=weekday + 1)  # 上周日
    last_monday = last_sunday - timedelta(days=6)  # 上周一
    
    return last_monday.strftime("%Y-%m-%d"), last_sunday.strftime("%Y-%m-%d")


def parse_archive_file(file_path: Path) -> list[dict]:
    """
    解析归档文件，提取文章信息
    
    参数:
        file_path: 归档文件路径
    
    返回:
        文章列表，每篇文章包含 title, url, score, comments
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        articles = []
        
        # 匹配格式: 1. [title](url) - score points, comments comments
        pattern = r'\d+\.\s+\[(.+?)\]\((.+?)\)\s+-\s+(\d+)\s+points,\s+(\d+)\s+comments'
        matches = re.findall(pattern, content)
        
        for title, url, score, comments in matches:
            articles.append({
                "title": title,
                "url": url,
                "score": int(score),
                "comments": int(comments)
            })
        
        return articles
    except Exception:
        return []


def collect_week_articles(start_date: str, end_date: str) -> list[dict]:
    """
    收集一周内的所有文章
    
    参数:
        start_date: 开始日期 YYYY-MM-DD
        end_date: 结束日期 YYYY-MM-DD
    
    返回:
        所有文章列表
    """
    archives_dir = Path("archives")
    all_articles = []
    
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    current = start
    while current <= end:
        file_path = archives_dir / f"{current.strftime('%Y-%m-%d')}.md"
        if file_path.exists():
            articles = parse_archive_file(file_path)
            all_articles.extend(articles)
        current += timedelta(days=1)
    
    return all_articles


def rank_articles(articles: list[dict], top_n: int = 20) -> list[dict]:
    """
    对文章进行排名（按分数降序）
    
    参数:
        articles: 文章列表
        top_n: 返回前N篇
    
    返回:
        排名后的文章列表
    """
    # 去重（相同URL只保留分数最高的）
    unique_articles = {}
    for article in articles:
        url = article["url"]
        if url not in unique_articles or article["score"] > unique_articles[url]["score"]:
            unique_articles[url] = article
    
    # 按分数排序
    sorted_articles = sorted(unique_articles.values(), key=lambda x: x["score"], reverse=True)
    
    return sorted_articles[:top_n]


def generate_weekly_content(start_date: str, end_date: str, top_articles: list[dict]) -> str:
    """
    生成周报内容
    
    参数:
        start_date: 开始日期
        end_date: 结束日期
        top_articles: 热门文章列表
    
    返回:
        Markdown 格式的周报内容
    """
    lines = []
    
    # 为文章添加标签
    for article in top_articles:
        add_tags_to_article(article)
    
    # 标题
    lines.append(f"# 📊 Hacker News 周报")
    lines.append(f"## {start_date} 至 {end_date}")
    lines.append("")
    
    # 统计信息
    lines.append("### 📈 本周统计")
    lines.append("")
    total_score = sum(article["score"] for article in top_articles)
    total_comments = sum(article["comments"] for article in top_articles)
    lines.append(f"- 📝 收录文章：{len(top_articles)} 篇")
    lines.append(f"- ⭐ 总点赞数：{total_score:,}")
    lines.append(f"- 💬 总评论数：{total_comments:,}")
    lines.append("")
    
    # 标签统计
    tag_stats = get_tag_statistics(top_articles)
    lines.append("### 🏷️ 热门标签")
    lines.append("")
    for tag, count in list(tag_stats.items())[:5]:  # 显示前5个标签
        lines.append(f"- {format_tags_for_display([tag])}: {count} 篇")
    lines.append("")
    
    # Top 20 文章
    lines.append("### 🔥 本周 Top 20 热门文章")
    lines.append("")
    
    for i, article in enumerate(top_articles, 1):
        title = article["title"]
        url = article["url"]
        score = article["score"]
        comments = article["comments"]
        tags = format_tags_for_display(article.get("tags", []))
        
        lines.append(f"{i}. [{title}]({url})")
        lines.append(f"   - ⭐ {score} points | 💬 {comments} comments")
        if tags:
            lines.append(f"   - {tags}")
        lines.append("")
    
    # 页脚
    lines.append("---")
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz)
    timestamp = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"*周报生成时间: {timestamp} (北京时间)*")
    lines.append("*数据来源: [Hacker News API](https://github.com/HackerNews/API)*")
    
    return "\n".join(lines)


def update_readme_weekly_section(weekly_summary: str) -> None:
    """
    更新 README 中的周报区域
    
    参数:
        weekly_summary: 周报摘要内容（简化版）
    """
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        return
    
    content = readme_path.read_text(encoding="utf-8")
    
    # 如果没有周报区域标记，在日报区域后添加
    if "<!-- WEEKLY_SUMMARY_START -->" not in content:
        # 在日报区域后添加周报区域
        daily_end = content.find("<!-- DAILY_ARTICLES_END -->")
        if daily_end != -1:
            insert_pos = content.find("\n---\n", daily_end)
            if insert_pos != -1:
                weekly_section = f"\n\n## 📊 本周热门\n\n<!-- WEEKLY_SUMMARY_START -->\n{weekly_summary}\n<!-- WEEKLY_SUMMARY_END -->\n"
                content = content[:insert_pos] + weekly_section + content[insert_pos:]
    else:
        # 更新现有周报区域
        pattern = r'<!-- WEEKLY_SUMMARY_START -->.*?<!-- WEEKLY_SUMMARY_END -->'
        replacement = f'<!-- WEEKLY_SUMMARY_START -->\n{weekly_summary}\n<!-- WEEKLY_SUMMARY_END -->'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    readme_path.write_text(content, encoding="utf-8")


def generate_weekly_summary() -> None:
    """
    生成周报的主函数
    """
    print("=" * 50)
    print("Weekly Summary - 开始生成周报")
    print("=" * 50)
    print()
    
    # 获取本周日期范围
    start_date, end_date = get_week_date_range()
    print(f"周期: {start_date} 至 {end_date}")
    print()
    
    # 收集本周文章
    print("步骤 1: 收集本周文章")
    all_articles = collect_week_articles(start_date, end_date)
    print(f"共收集 {len(all_articles)} 篇文章")
    print()
    
    if not all_articles:
        print("⚠️  本周暂无文章数据")
        return
    
    # 排名文章
    print("步骤 2: 文章排名")
    top_articles = rank_articles(all_articles, top_n=20)
    print(f"Top 20 文章已选出")
    print()
    
    # 生成周报文件
    print("步骤 3: 生成周报文件")
    weekly_content = generate_weekly_content(start_date, end_date, top_articles)
    
    # 保存周报文件
    weekly_dir = Path("weekly")
    weekly_dir.mkdir(exist_ok=True)
    
    # 使用周日日期作为文件名
    weekly_file = weekly_dir / f"week-{end_date}.md"
    weekly_file.write_text(weekly_content, encoding="utf-8")
    print(f"周报文件已保存: {weekly_file}")
    print()
    
    # 生成README摘要（Top 10）
    print("步骤 4: 更新 README")
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz)
    timestamp = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
    
    summary_lines = [f"> 🕐 最后更新：{timestamp} (北京时间)", ""]
    summary_lines.append(f"**本周热门 ({start_date} 至 {end_date})**")
    summary_lines.append("")
    
    for i, article in enumerate(top_articles[:10], 1):
        tags = format_tags_for_display(article.get("tags", []))
        summary_lines.append(f"{i}. [{article['title']}]({article['url']}) - {article['score']} points, {article['comments']} comments")
        if tags:
            summary_lines.append(f"   - {tags}")
    
    summary_lines.append("")
    summary_lines.append(f"📁 **[查看完整周报](weekly/week-{end_date}.md)** | Top 20 热门文章")
    
    update_readme_weekly_section("\n".join(summary_lines))
    print("README 已更新")
    print()
    
    print("=" * 50)
    print("✓ 周报生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    generate_weekly_summary()
