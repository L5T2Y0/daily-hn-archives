# Daily HN Archives - 主入口点
"""
Daily Hacker News Archives
每天自动获取并归档 Hacker News 的 Top 10 热门文章
"""
import sys
from datetime import datetime
from hn_fetcher import fetch_top_stories
from markdown_generator import generate_archive_content, generate_readme_content
from file_manager import write_archive_file, get_archive_files, write_readme


def main() -> int:
    """
    主函数，执行完整的归档流程
    
    返回:
        退出码（0 表示成功，非 0 表示失败）
    """
    try:
        print("=" * 50)
        print("Daily HN Archives - 开始执行")
        print("=" * 50)
        
        # 获取当前日期
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\n日期: {today}")
        
        # 获取文章列表
        print("\n步骤 1: 获取 Hacker News Top 10 文章")
        stories = fetch_top_stories(10)
        
        if not stories:
            print("错误: 未能获取任何文章", file=sys.stderr)
            return 1
        
        print(f"成功获取 {len(stories)} 篇文章")
        
        # 生成归档内容
        print("\n步骤 2: 生成归档内容")
        archive_content = generate_archive_content(stories, today)
        
        # 写入归档文件
        print("\n步骤 3: 写入归档文件")
        write_archive_file(today, archive_content)
        
        # 获取所有归档文件
        print("\n步骤 4: 获取历史归档列表")
        archive_files = get_archive_files()
        print(f"找到 {len(archive_files)} 个归档文件")
        
        # 生成 README 内容
        print("\n步骤 5: 生成 README 内容")
        readme_content = generate_readme_content(stories, archive_files)
        
        # 更新 README
        print("\n步骤 6: 更新 README.md")
        write_readme(readme_content)
        
        print("\n" + "=" * 50)
        print("✓ 归档完成！")
        print("=" * 50)
        
        return 0
        
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
