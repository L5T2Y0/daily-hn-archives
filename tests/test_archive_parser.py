"""
测试 archive_parser 模块
"""

from archive_parser import parse_archive_file


class TestParseArchiveFile:
    """测试归档文件解析函数"""

    def test_parse_valid_archive_file(self, tmp_path):
        """测试解析有效的归档文件"""
        # 创建测试文件
        test_file = tmp_path / "2026-03-15.md"
        content = """# Hacker News Top 10 - 2026-03-15

1. [Test Article 1](https://example.com/1) - 123 points, 45 comments
2. [Test Article 2](https://example.com/2) - 89 points, 23 comments
3. [Test Article 3](https://example.com/3) - 67 points, 12 comments

---
*归档生成时间: 2026-03-15 08:30:15*
"""
        test_file.write_text(content, encoding="utf-8")

        # 解析文件
        result = parse_archive_file(test_file)

        # 验证结果
        assert len(result) == 3

        assert result[0]["title"] == "Test Article 1"
        assert result[0]["url"] == "https://example.com/1"
        assert result[0]["score"] == 123
        assert result[0]["comments"] == 45
        assert result[0]["date"] == "2026-03-15"

        assert result[1]["title"] == "Test Article 2"
        assert result[1]["score"] == 89
        assert result[1]["comments"] == 23

    def test_parse_empty_file(self, tmp_path):
        """测试解析空文件"""
        test_file = tmp_path / "2026-03-15.md"
        test_file.write_text("", encoding="utf-8")

        result = parse_archive_file(test_file)
        assert result == []

    def test_parse_nonexistent_file(self, tmp_path):
        """测试解析不存在的文件"""
        test_file = tmp_path / "nonexistent.md"

        result = parse_archive_file(test_file)
        assert result == []

    def test_date_extraction_from_filename(self, tmp_path):
        """测试从文件名提取日期"""
        test_file = tmp_path / "2026-12-31.md"
        content = """1. [Test Article](https://example.com) - 100 points, 20 comments"""
        test_file.write_text(content, encoding="utf-8")

        result = parse_archive_file(test_file)
        assert len(result) == 1
        assert result[0]["date"] == "2026-12-31"
        
