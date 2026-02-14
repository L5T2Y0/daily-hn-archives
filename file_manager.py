# File Manager 模块 - 负责文件操作
from pathlib import Path


def ensure_directory_exists(directory: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    参数:
        directory: 目录路径
    """
    path = Path(directory)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"创建目录失败 {directory}: {e}")
        raise



def write_archive_file(date: str, content: str) -> str:
    """
    写入归档文件
    
    参数:
        date: 日期字符串（YYYY-MM-DD）
        content: Markdown 内容
    
    返回:
        写入的文件路径
    """
    ensure_directory_exists("archives")
    
    file_path = Path("archives") / f"{date}.md"
    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"归档文件已写入: {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"写入归档文件失败 {file_path}: {e}")
        raise


def get_archive_files() -> list[str]:
    """
    获取所有归档文件列表，按日期倒序排列
    
    返回:
        归档文件名列表（不含路径）
    """
    archives_dir = Path("archives")
    
    if not archives_dir.exists():
        return []
    
    # 获取所有 .md 文件
    md_files = list(archives_dir.glob("*.md"))
    
    # 提取文件名并排序（倒序）
    file_names = [f.name for f in md_files]
    file_names.sort(reverse=True)
    
    return file_names


def write_readme(content: str) -> None:
    """
    写入 README.md 文件
    
    参数:
        content: README 内容
    """
    readme_path = Path("README.md")
    try:
        readme_path.write_text(content, encoding="utf-8")
        print(f"README 已更新: {readme_path}")
    except Exception as e:
        print(f"写入 README 失败: {e}")
        raise
