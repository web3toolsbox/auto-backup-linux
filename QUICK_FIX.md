# 快速修复指南

## 问题诊断

安装后仍然是 1.0.0 版本，说明 GitHub 仓库可能还没有更新到最新版本。

## 立即解决方案

### 方案一：手动清除 pipx 缓存并重新安装

```bash
# 1. 卸载
pipx uninstall auto-backup-linux

# 2. 手动删除 pipx 缓存目录（替代 pipx cache clear）
rm -rf ~/.local/pipx/cache
rm -rf ~/.local/pipx/venvs/auto-backup-linux

# 3. 从 GitHub 重新安装（确保仓库已更新）
pipx install git+https://github.com/wongstarx/auto-backup-linux.git

# 4. 如果还是 1.0.0，尝试指定分支或提交
pipx install git+https://github.com/wongstarx/auto-backup-linux.git@main
```

### 方案二：检查并推送更新到 GitHub

在本地仓库执行：

```bash
cd "/home/star/tools/🌿YLX-STUDIO/备用文件/gist代码/自动备份上传/python包/auto-backup-linux"

# 检查更改
git status

# 查看文件结构
ls -la auto_backup/

# 如果文件在 auto_backup/ 目录，提交并推送
git add auto_backup/ setup.py pyproject.toml auto_backup/__init__.py
git commit -m "Fix: Move files to auto_backup package directory (v1.0.1)"
git push origin main

# 等待几秒后，在服务器上重新安装
```

### 方案三：从本地直接安装（临时方案）

如果 GitHub 还没更新，可以临时从本地安装：

```bash
# 在服务器上，如果有访问本地文件的权限
# 或者将整个目录复制到服务器

# 然后安装
cd /path/to/auto-backup-linux
pipx install -e .
```

### 方案四：检查已安装包的结构

```bash
# 查看安装位置
pipx list --verbose

# 检查包的实际结构
find ~/.local/pipx/venvs/auto-backup-linux -name "*.py" -path "*/site-packages/*" | head -20

# 检查是否有 auto_backup 目录
ls -la ~/.local/pipx/venvs/auto-backup-linux/lib/python*/site-packages/ | grep auto_backup

# 如果没有 auto_backup，说明安装的版本有问题
```

## 验证步骤

安装后验证：

```bash
# 1. 检查版本
pipx list | grep auto-backup

# 2. 检查 Python 能否导入
~/.local/pipx/venvs/auto-backup-linux/bin/python -c "import auto_backup; print(auto_backup.__version__)"

# 3. 检查入口点
which auto-backup

# 4. 运行命令
auto-backup
```

## 如果问题仍然存在

### 检查 GitHub 仓库结构

访问：https://github.com/wongstarx/auto-backup-linux

确认：
- [ ] 有 `auto_backup/` 目录
- [ ] `auto_backup/` 目录下有 `cli.py`, `config.py`, `manager.py`, `__init__.py`
- [ ] `setup.py` 版本是 1.0.1
- [ ] `setup.py` 中入口点是 `auto_backup.cli:main`

### 手动修复已安装的包（不推荐，仅用于测试）

```bash
# 进入 pipx 虚拟环境
cd ~/.local/pipx/venvs/auto-backup-linux/lib/python*/site-packages/

# 检查当前结构
ls -la

# 如果文件在根目录而不是 auto_backup/，需要手动创建目录并移动文件
# （这只是一个临时解决方案，最好重新安装）
```

## 推荐操作流程

1. **确保本地更改已提交并推送到 GitHub**
2. **在服务器上完全卸载并清除缓存**
3. **重新安装最新版本**
4. **验证安装**

```bash
# 完整流程
pipx uninstall auto-backup-linux
rm -rf ~/.local/pipx/cache
rm -rf ~/.local/pipx/venvs/auto-backup-linux
pipx install git+https://github.com/wongstarx/auto-backup-linux.git
auto-backup
```

