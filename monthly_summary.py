# Monthly Summary 模块 - 负责生成月报
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
from archive_parser import parse_archive_file
from tag_classifier import add_tags_to_article, group_articles_by_tag, get_tag_statistics, format_tags_for_display


def get_last_month_range() -> tuple[str, str]:
    """
    获取上个月整月的日期范围

    返回:
        (start_date, end_date) 格式为 YYYY-MM-DD
    """
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).date()

    # 本月第一天
    first_day_this_month = today.replace(day=1)

    # 上个月最后一天 = 本月第一天 - 1 天
    last_day_last_month = first_day_this_month - timedelta(days=1)

    # 上个月第一天
    first_day_last_month = last_day_last_month.replace(day=1)

    return first_day_last_month.strftime("%Y-%m-%d"), last_day_last_month.strftime("%Y-%m-%d")


def collect_month_articles(start_date: str, end_date: str) -> list[dict]:
    """
    收集周期内的所有文章

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


def rank_articles(articles: list[dict], top_n: int = 50) -> list[dict]:
    """
    对文章进行排名（按分数降序）

    参数:
        articles: 文章列表
        top_n: 返回前N篇

    返回:
        排名后的文章列表
    """
    # 去重（相同URL只保留分数最高的）
    unique_articles: dict[str, dict] = {}
    for article in articles:
        url = article["url"]
        if url not in unique_articles or article["score"] > unique_articles[url]["score"]:
            unique_articles[url] = article

    # 按分数排序
    sorted_articles = sorted(unique_articles.values(), key=lambda x: x["score"], reverse=True)

    return sorted_articles[:top_n]


def generate_monthly_content(start_date: str, end_date: str, top_articles: list[dict]) -> str:
    """
    生成月报内容

    参数:
        start_date: 开始日期
        end_date: 结束日期
        top_articles: 热门文章列表

    返回:
        Markdown 格式的月报内容
    """
    lines = []

    # 为文章添加标签
    for article in top_articles:
        add_tags_to_article(article)

    # 提取年月（以开始日期为准：上个月）
    year_month = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y年%m月")

    # 标题
    lines.append("# 📊 Hacker News 月报")
    lines.append(f"## {year_month}精选")
    lines.append(f"### {start_date} 至 {end_date}")
    lines.append("")

    # 统计信息
    lines.append("### 📈 本月统计")
    lines.append("")
    total_score = sum(article["score"] for article in top_articles)
    total_comments = sum(article["comments"] for article in top_articles)
    avg_score = total_score // len(top_articles) if top_articles else 0
    lines.append(f"- 📝 收录文章：{len(top_articles)} 篇")
    lines.append(f"- ⭐ 总点赞数：{total_score:,}")
    lines.append(f"- 💬 总评论数：{total_comments:,}")
    lines.append(f"- 📊 平均点赞：{avg_score} points")
    lines.append("")

    # 标签统计
    tag_stats = get_tag_statistics(top_articles)
    lines.append("### 🏷️ 热门标签")
    lines.append("")
    for tag, count in list(tag_stats.items())[:8]:  # 显示前8个标签
        lines.append(f"- {format_tags_for_display([tag])}: {count} 篇")
    lines.append("")

    # 按标签分组
    grouped = group_articles_by_tag(top_articles)
    lines.append("### 📂 分类浏览")
    lines.append("")
    for tag in list(tag_stats.keys())[:5]:  # 显示前5个分类
        if tag in grouped:
            lines.append(f"#### {format_tags_for_display([tag])} ({len(grouped[tag])} 篇)")
            lines.append("")
            for article in grouped[tag][:5]:  # 每个分类显示前5篇
                lines.append(f"- [{article['title']}]({article['url']}) - {article['score']} points")
            lines.append("")

    # Top 50 文章
    lines.append("### 🔥 Top 50 热门文章")
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
    lines.append(f"*月报生成时间: {timestamp} (北京时间)*")
    lines.append("*数据来源: [Hacker News API](https://github.com/HackerNews/API)*")

    return "\n".join(lines)


def update_readme_monthly_section(monthly_summary: str) -> None:
    """
    更新 README 中的月报区域

    参数:
        monthly_summary: 月报摘要内容（简化版）
    """
    readme_path = Path("README.md")

    if not readme_path.exists():
        return

    content = readme_path.read_text(encoding="utf-8")

    # 如果没有月报区域标记，在周报区域后添加
    if "<!-- MONTHLY_SUMMARY_START -->" not in content:
        # 在周报区域后添加月报区域
        weekly_end = content.find("<!-- WEEKLY_SUMMARY_END -->")
        if weekly_end != -1:
            insert_pos = content.find("\n---\n", weekly_end)
            if insert_pos != -1:
                monthly_section = (
                    "\n\n## 📅 本月精选\n\n<!-- MONTHLY_SUMMARY_START -->\n"
                    + monthly_summary
                    + "\n<!-- MONTHLY_SUMMARY_END -->\n"
                )
                content = content[:insert_pos] + monthly_section + content[insert_pos:]
    else:
        # 更新现有月报区域
        pattern = r"<!-- MONTHLY_SUMMARY_START -->.*?<!-- MONTHLY_SUMMARY_END -->"
        replacement = f"<!-- MONTHLY_SUMMARY_START -->\n{monthly_summary}\n<!-- MONTHLY_SUMMARY_END -->"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    readme_path.write_text(content, encoding="utf-8")


def generate_monthly_summary() -> None:
    """
    生成月报的主函数
    """
    print("=" * 50)
    print("Monthly Summary - 开始生成月报")
    print("=" * 50)
    print()

    # 获取上个月整月日期范围
    start_date, end_date = get_last_month_range()
    year_month = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y年%m月")
    print(f"周期: {year_month} ({start_date} 至 {end_date})")
    print()

    # 收集周期文章
    print("步骤 1: 收集周期文章")
    all_articles = collect_month_articles(start_date, end_date)
    print(f"共收集 {len(all_articles)} 篇文章")
    print()

    if not all_articles:
        print("⚠️  暂无文章数据")
        return

    # 排名文章
    print("步骤 2: 文章排名")
    top_articles = rank_articles(all_articles, top_n=50)
    print("Top 50 文章已选出")
    print()

    # 生成月报文件
    print("步骤 3: 生成月报文件")
    monthly_content = generate_monthly_content(start_date, end_date, top_articles)

    # 保存月报文件（使用上个月 YYYY-MM）
    monthly_dir = Path("monthly")
    monthly_dir.mkdir(exist_ok=True)

    month_str = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m")
    monthly_file = monthly_dir / f"month-{month_str}.md"
    monthly_file.write_text(monthly_content, encoding="utf-8")
    print(f"月报文件已保存: {monthly_file}")
    print()

    # 生成 README 摘要（Top 10）
    print("步骤 4: 更新 README")
    beijing_tz = timezone(timedelta(hours=8))
    beijing_time = datetime.now(beijing_tz)
    timestamp = beijing_time.strftime("%Y-%m-%d %H:%M:%S")

    summary_lines = [f"> 🕐 最后更新：{timestamp} (北京时间)", ""]
    summary_lines.append(f"**{year_month}精选**")
    summary_lines.append("")

    for i, article in enumerate(top_articles[:10], 1):
        tags = format_tags_for_display(article.get("tags", []))
        summary_lines.append(
            f"{i}. [{article['title']}]({article['url']}) - {article['score']} points, {article['comments']} comments"
        )
        if tags:
            summary_lines.append(f"   - {tags}")

    summary_lines.append("")
    summary_lines.append(f"📁 **[查看完整月报](monthly/month-{month_str}.md)** | Top 50 热门文章")

    update_readme_monthly_section("\n".join(summary_lines))
    print("README 已更新")
    print()

    print("=" * 50)
    print("✓ 月报生成完成！")
    print("=" * 50)


if __name__ == "__main__":
    generate_monthly_summary()
