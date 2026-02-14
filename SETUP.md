# 项目设置指南

## 📦 上传到 GitHub

### 1. 初始化仓库

```bash
# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial commit: Daily HN Archives"
```

### 2. 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 创建新仓库（建议命名为 `daily-hn-archives`）
3. **不要**初始化 README、.gitignore 或 LICENSE

### 3. 推送代码

```bash
# 关联远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/daily-hn-archives.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 4. 启用 GitHub Actions

1. 进入仓库 → `Settings` → `Actions` → `General`
2. 在 "Workflow permissions" 部分选择 `Read and write permissions`
3. 保存设置

### 5. 测试运行

1. 进入 `Actions` 标签页
2. 选择 `Daily HN Archives Update` workflow
3. 点击 `Run workflow` → `Run workflow` 按钮
4. 等待运行完成，检查是否成功

## 🎨 自定义项目说明

将 `PROJECT_DESCRIPTION.md` 的内容复制到 GitHub 仓库的描述中：

1. 打开 `PROJECT_DESCRIPTION.md`
2. 复制全部内容
3. 在 GitHub 仓库页面，点击 `Add a README` 或编辑现有 README
4. 粘贴内容
5. 替换所有 `YOUR_USERNAME` 为你的 GitHub 用户名
6. 替换 `YOUR_NAME` 为你的名字
7. 替换 `your.email@example.com` 为你的邮箱（可选）
8. 提交更改

**注意**：不要在本地创建 README.md，因为程序会自动生成它。

## ⚙️ 配置说明

### 修改运行时间

编辑 `.github/workflows/daily_run.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0点 = 北京时间 8点
```

常用时间：
- `0 0 * * *` - 每天 UTC 0点（北京时间 8点）
- `0 16 * * *` - 每天 UTC 16点（北京时间 0点）
- `0 12 * * *` - 每天 UTC 12点（北京时间 20点）

### 修改文章数量

编辑 `main.py`，找到：

```python
stories = fetch_top_stories(10)  # 改为你想要的数量
```

## 🔍 故障排查

### Actions 运行失败

1. 检查 Actions 日志查看具体错误
2. 确认仓库有写入权限（见上面的步骤 4）
3. 手动触发测试是否成功

### 没有自动提交

1. 确认 workflow 运行成功
2. 检查是否有文件变动（可能当天已经运行过）
3. 查看 Actions 日志中的 "Check for changes" 步骤

## 📝 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行脚本
python main.py

# 查看生成的文件
ls archives/
cat README.md
```

## 🗑️ 清理说明

上传到 GitHub 后，以下文件/目录会被自动忽略（已在 .gitignore 中）：
- `.kiro/` - Kiro 的 spec 文档
- `.vscode/`, `.idea/` - IDE 配置
- `__pycache__/` - Python 缓存
- `PROJECT_DESCRIPTION.md` - 项目说明模板

这些文件不会被提交到 GitHub，保持仓库整洁。
