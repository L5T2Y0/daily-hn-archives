# 贡献指南

感谢你对 Daily HN Archives 项目的关注！我们欢迎所有形式的贡献。

## 🤝 如何贡献

### 报告 Bug

如果你发现了 bug，请：
1. 在 [Issues](https://github.com/L5T2Y0/daily-hn-archives/issues) 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（Python 版本、操作系统等）

### 提出新功能

如果你有新功能建议：
1. 在 Issues 中创建 Feature Request
2. 描述功能的用途和价值
3. 如果可能，提供实现思路

### 提交代码

1. **Fork 项目**
   ```bash
   # 点击 GitHub 页面右上角的 Fork 按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/daily-hn-archives.git
   cd daily-hn-archives
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行修改**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新相关文档

5. **测试**
   ```bash
   python main.py  # 确保程序正常运行
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 简短描述你的更改"
   ```

7. **推送到 GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上打开你的 fork
   - 点击 "New Pull Request"
   - 填写 PR 描述

## 📝 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 4 空格缩进
- 函数和类添加文档字符串
- 变量命名使用小写加下划线

### 提交信息规范

使用清晰的提交信息：
- `Add: 添加新功能`
- `Fix: 修复 bug`
- `Update: 更新现有功能`
- `Refactor: 重构代码`
- `Docs: 更新文档`
- `Style: 代码格式调整`

## 🧪 测试

在提交 PR 前，请确保：
- [ ] 代码能够正常运行
- [ ] 没有引入新的错误
- [ ] 更新了相关文档

## 📄 许可证

提交代码即表示你同意将代码以 MIT 许可证发布。

## 💬 需要帮助？

如有任何问题，欢迎：
- 在 Issues 中提问
- 查看现有的 Issues 和 PR
- 阅读项目文档

感谢你的贡献！🎉
