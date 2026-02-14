<div align="center">

# 📰 Daily Hacker News Archives

### 每天自动归档 Hacker News 热门文章

[![Daily Update](https://github.com/L5T2Y0/daily-hn-archives/actions/workflows/daily_run.yml/badge.svg)](https://github.com/L5T2Y0/daily-hn-archives/actions/workflows/daily_run.yml)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/L5T2Y0/daily-hn-archives?style=social)](https://github.com/L5T2Y0/daily-hn-archives/stargazers)

[English](#) | [简体中文](#)

</div>

---

## 📖 项目简介

这是一个基于 **GitHub Actions** 的自动化项目，每天定时获取 [Hacker News](https://news.ycombinator.com/) 的 Top 10 热门文章，并以 Markdown 格式归档保存。

通过这个项目，你可以：
- 📚 **追踪科技趋势**：每天了解技术圈最热门的话题
- 🌱 **保持活跃**：自动提交让你的 GitHub 贡献图保持绿色
- 🎓 **学习实践**：了解 GitHub Actions、Python 爬虫、API 调用等技术
- 🔧 **自由扩展**：模块化设计，轻松添加新功能

## ✨ 核心特性

<table>
<tr>
<td width="50%">

### 🤖 全自动运行
- 每天 UTC 0点自动执行
- 无需人工干预
- 失败自动重试机制

</td>
<td width="50%">

### 📁 智能归档
- 按日期独立存储
- Markdown 格式易读
- 包含完整元数据

</td>
</tr>
<tr>
<td width="50%">

### 📊 动态索引
- README 自动更新
- 历史记录一目了然
- 支持快速检索

</td>
<td width="50%">

### 🌱 GitHub 集成
- 每日自动提交
- 贡献图保持活跃
- 完整的 CI/CD 流程

</td>
</tr>
</table>

## 🎬 效果预览

### 归档文件示例

```markdown
# Hacker News Top 10 - 2026-02-14

1. [Show HN: I built a tool that...](https://example.com) - 523 points, 127 comments
2. [The Future of AI Development](https://example.com) - 456 points, 89 comments
3. [Why Rust is the Future](https://example.com) - 398 points, 156 comments
...

---
*归档生成时间: 2026-02-14 08:30:15*
*数据来源: Hacker News API*
```

### README 自动更新

项目的 README.md 会自动展示：
- ✅ 今日 Top 10 文章列表
- ✅ 历史归档索引（按日期倒序）
- ✅ 最后更新时间戳

### GitHub Actions 运行日志

<details>
<summary>点击查看运行日志示例</summary>

```
==================================================
Daily HN Archives - 开始执行
==================================================

日期: 2026-02-14

步骤 1: 获取 Hacker News Top 10 文章
正在获取 Top 10 文章...
  已获取文章 1/10
  已获取文章 2/10
  ...
成功获取 10 篇文章

步骤 2: 生成归档内容
步骤 3: 写入归档文件
归档文件已写入: archives/2026-02-14.md

步骤 4: 获取历史归档列表
找到 45 个归档文件

步骤 5: 生成 README 内容
步骤 6: 更新 README.md
README 已更新: README.md

==================================================
✓ 归档完成！
==================================================
```

</details>

---

## 📂 项目结构

```
daily-hn-archives/
├── 📄 main.py                 # 主入口点，协调整个流程
├── 🔌 hn_fetcher.py          # HN API 交互模块（含重试机制）
├── 📝 markdown_generator.py  # Markdown 内容生成模块
├── 💾 file_manager.py        # 文件操作模块（UTF-8 编码）
├── 📋 requirements.txt       # Python 依赖列表
├── 📁 archives/              # 归档文件目录
│   ├── 2026-02-14.md        # 每日归档文件
│   ├── 2026-02-13.md
│   └── ...
├── 📖 README.md              # 项目主页（自动生成）
└── ⚙️ .github/
    └── workflows/
        └── daily_run.yml     # GitHub Actions 自动化配置
```

### 模块说明

| 模块 | 功能 | 关键特性 |
|------|------|----------|
| `hn_fetcher.py` | 与 Hacker News API 交互 | 自动重试、超时处理、错误恢复 |
| `markdown_generator.py` | 生成 Markdown 内容 | 格式化文章、生成索引、时间戳 |
| `file_manager.py` | 文件系统操作 | UTF-8 编码、目录管理、文件排序 |
| `main.py` | 流程协调 | 错误处理、进度输出、退出码管理 |

## 🚀 快速开始

### 方式一：Fork 并自动运行（推荐）

1. **Fork 本仓库**
   
   点击右上角的 `Fork` 按钮

2. **启用 GitHub Actions**
   
   进入你的仓库 → `Settings` → `Actions` → `General`
   
   确保 `Allow all actions and reusable workflows` 已启用

3. **手动触发测试**
   
   进入 `Actions` 标签页 → 选择 `Daily HN Archives Update` → 点击 `Run workflow`

4. **等待自动运行**
   
   每天 UTC 0点自动执行，无需任何操作！

### 方式二：本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/L5T2Y0/daily-hn-archives.git
cd daily-hn-archives

# 2. 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行脚本
python main.py
```

### 方式三：从零开始部署

<details>
<summary>点击展开详细步骤</summary>

```bash
# 1. 创建新目录
mkdir daily-hn-archives
cd daily-hn-archives

# 2. 初始化 git
git init

# 3. 复制项目文件到此目录

# 4. 首次提交
git add .
git commit -m "Initial commit: Daily HN Archives"

# 5. 在 GitHub 创建新仓库（通过网页）

# 6. 关联远程仓库
git remote add origin https://github.com/L5T2Y0/REPO_NAME.git

# 7. 推送到 GitHub
git branch -M main
git push -u origin main

# 8. 启用 Actions（参考方式一的步骤 2）
```

</details>

## 📋 归档格式

每个归档文件包含：
- 日期标题
- Top 10 文章列表（标题、链接、分数、评论数）
- 生成时间戳
- 数据来源说明

示例：
```markdown
# Hacker News Top 10 - 2026-02-14

1. [Article Title](https://example.com) - 123 points, 45 comments
2. [Another Article](https://example.com) - 120 points, 38 comments
...
```

## 🔧 技术栈

<div align="center">

| 技术 | 用途 | 版本要求 |
|:----:|:----:|:--------:|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | 核心语言 | 3.7+ |
| ![Requests](https://img.shields.io/badge/Requests-FF6F00?style=for-the-badge) | HTTP 请求 | 2.31.0+ |
| ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) | CI/CD 自动化 | - |
| ![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white) | 文档格式 | - |

</div>

### 核心依赖

- **requests**: 用于发送 HTTP 请求到 Hacker News API
  - 支持超时设置
  - 自动重试机制
  - 异常处理

### API 说明

本项目使用 [Hacker News Official API](https://github.com/HackerNews/API)：

- **Top Stories 端点**: `https://hacker-news.firebaseio.com/v0/topstories.json`
  - 返回热门文章 ID 列表
  
- **Item 详情端点**: `https://hacker-news.firebaseio.com/v0/item/{id}.json`
  - 返回文章详细信息（标题、链接、分数、评论数等）

## 🎯 Roadmap

### ✅ 已完成

- [x] 基础功能实现
- [x] GitHub Actions 自动化
- [x] 错误处理和重试机制
- [x] UTF-8 编码支持
- [x] 模块化架构设计

### 🚧 进行中

- [ ] 添加单元测试
- [ ] 完善错误日志
- [ ] 优化性能

### 📅 计划中

#### 短期目标（1-2 个月）

- [ ] **周报功能**：每周日生成一周热门文章汇总
- [ ] **月报功能**：每月生成月度热门文章排行
- [ ] **标签分类**：自动识别文章类别（AI、Web、DevOps 等）
- [ ] **搜索功能**：支持关键词搜索历史文章

#### 中期目标（3-6 个月）

- [ ] **数据可视化**：生成热门话题趋势图
- [ ] **RSS Feed**：提供 RSS 订阅功能
- [ ] **邮件通知**：支持邮件订阅每日摘要
- [ ] **多语言支持**：添加英文界面
- [ ] **评论分析**：统计最热门的评论

#### 长期目标（6+ 个月）

- [ ] **多源聚合**：支持 Reddit、Product Hunt 等其他平台
- [ ] **AI 摘要**：使用 AI 生成文章摘要
- [ ] **个性化推荐**：基于用户兴趣推荐文章
- [ ] **Web 界面**：开发在线浏览界面
- [ ] **移动应用**：开发移动端 App

### 💡 功能建议

欢迎在 [Issues](https://github.com/L5T2Y0/daily-hn-archives/issues) 中提出你的想法！

## ❓ 常见问题

<details>
<summary><b>Q: 为什么选择 UTC 0点运行？</b></summary>

A: UTC 0点对应北京时间早上 8点，这样可以在工作日开始时看到最新的文章。你可以在 `.github/workflows/daily_run.yml` 中修改 cron 表达式来调整时间。

</details>

<details>
<summary><b>Q: 如何修改获取的文章数量？</b></summary>

A: 在 `main.py` 中找到 `fetch_top_stories(10)` 这一行，将 `10` 改为你想要的数量即可。

</details>

<details>
<summary><b>Q: GitHub Actions 运行失败怎么办？</b></summary>

A: 
1. 检查 Actions 日志查看具体错误
2. 确认仓库有写入权限（Settings → Actions → General → Workflow permissions）
3. 检查网络连接是否正常
4. 查看 Hacker News API 是否可访问

</details>

<details>
<summary><b>Q: 可以同时归档多个新闻源吗？</b></summary>

A: 当前版本只支持 Hacker News，但你可以参考代码结构添加其他新闻源。这是一个很好的扩展方向！

</details>

<details>
<summary><b>Q: 如何备份归档数据？</b></summary>

A: 所有数据都存储在 Git 仓库中，GitHub 会自动保存历史版本。你也可以定期克隆仓库到本地作为备份。

</details>

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是报告 bug、提出新功能建议，还是提交代码改进。

### 如何贡献

1. **Fork 本仓库**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启 Pull Request**

### 贡献类型

- 🐛 **报告 Bug**：在 Issues 中详细描述问题
- 💡 **功能建议**：分享你的创意想法
- 📝 **文档改进**：完善 README 或添加注释
- � **代码优化**：提升性能或代码质量
- 🌍 **翻译**：帮助添加多语言支持

### 开发规范

- 遵循 PEP 8 Python 代码规范
- 添加必要的注释和文档字符串
- 确保代码通过现有测试
- 新功能需要添加相应测试

---

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/L5T2Y0/daily-hn-archives)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/L5T2Y0/daily-hn-archives)
![GitHub last commit](https://img.shields.io/github/last-commit/L5T2Y0/daily-hn-archives)

</div>

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

```
MIT License

Copyright (c) 2026 梦宇

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📧 联系方式

<div align="center">

如有问题或建议，欢迎通过以下方式联系：

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-green?style=for-the-badge&logo=github)](https://github.com/L5T2Y0/daily-hn-archives/issues)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:l0t0y@vip.qq.com)

</div>

---

## 🌟 Star History

如果这个项目对你有帮助，请给个 Star ⭐️

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=L5T2Y0/daily-hn-archives&type=Date)](https://star-history.com/#L5T2Y0/daily-hn-archives&Date)

</div>

---

## 🙏 致谢

- [Hacker News](https://news.ycombinator.com/) - 提供优质的技术内容
- [Hacker News API](https://github.com/HackerNews/API) - 提供免费的 API 服务
- [GitHub Actions](https://github.com/features/actions) - 提供强大的自动化平台
- 所有贡献者和 Star 支持者 ❤️

---

<div align="center">

**[⬆ 回到顶部](#-daily-hacker-news-archives)**

Made with ❤️ by [梦宇](https://github.com/L5T2Y0)

⭐ **如果觉得有用，请给个 Star！** ⭐

</div>
