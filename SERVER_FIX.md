# 服务器端快速修复

## 问题
安装后仍然是 1.0.0 版本，且出现 `ModuleNotFoundError: No module named 'auto_backup'`

## 原因
GitHub 仓库可能还没有更新到包含修复的版本。

## 立即解决方案（在服务器上执行）

### 方法一：手动清除缓存并重新安装

```bash
# 1. 卸载
pipx uninstall auto-backup-linux

# 2. 手动删除缓存（pipx 没有 cache clear 命令）
rm -rf ~/.local/pipx/cache
rm -rf ~/.local/pipx/venvs/auto-backup-linux

# 3. 重新安装
pipx install git+https://github.com/wongstarx/auto-backup-linux.git

# 4. 验证
auto-backup
```

### 方法二：使用修复脚本

```bash
# 下载并运行修复脚本
curl -fsSL https://raw.githubusercontent.com/wongstarx/auto-backup-linux/main/INSTALL_FIX.sh | bash

# 或手动执行
bash <(curl -fsSL https://raw.githubusercontent.com/wongstarx/auto-backup-linux/main/INSTALL_FIX.sh)
```

### 方法三：检查并诊断

```bash
# 检查安装的包结构
pipx list --verbose | grep auto-backup

# 查看实际安装的文件
find ~/.local/pipx/venvs/auto-backup-linux -name "*.py" -path "*/site-packages/*" | grep -E "(cli|config|manager|__init__)"

# 检查是否有 auto_backup 目录
ls -la ~/.local/pipx/venvs/auto-backup-linux/lib/python*/site-packages/ | grep auto_backup

# 如果没有 auto_backup 目录，说明安装的版本有问题
```

### 方法四：从特定提交安装（如果知道修复的提交）

```bash
# 卸载
pipx uninstall auto-backup-linux

# 从最新提交安装
pipx install git+https://github.com/wongstarx/auto-backup-linux.git@main

# 或指定提交哈希
# pipx install git+https://github.com/wongstarx/auto-backup-linux.git@<commit-hash>
```

## 验证步骤

```bash
# 1. 检查版本（应该是 1.0.1）
pipx list | grep auto-backup

# 2. 测试 Python 导入
~/.local/pipx/venvs/auto-backup-linux/bin/python -c "import auto_backup; print('版本:', auto_backup.__version__)"

# 3. 检查命令
which auto-backup

# 4. 运行
auto-backup
```

## 如果仍然失败

### 检查 GitHub 仓库

访问 https://github.com/wongstarx/auto-backup-linux 并确认：

1. 是否有 `auto_backup/` 目录？
2. `setup.py` 版本是否是 1.0.1？
3. 入口点是否是 `auto_backup.cli:main`？

### 临时解决方案：手动修复已安装的包

```bash
# 进入 pipx 虚拟环境的 site-packages
cd ~/.local/pipx/venvs/auto-backup-linux/lib/python*/site-packages/

# 检查当前结构
ls -la

# 如果文件在根目录（cli.py, config.py 等），需要创建 auto_backup 目录并移动
mkdir -p auto_backup
mv __init__.py cli.py config.py manager.py auto_backup/ 2>/dev/null || true

# 测试
~/.local/pipx/venvs/auto-backup-linux/bin/python -c "import auto_backup; print('成功!')"
```

**注意**：这只是临时解决方案，最好重新安装正确版本。

## 推荐操作

1. **确保 GitHub 仓库已更新**（在本地推送更改）
2. **在服务器上完全清除并重新安装**
3. **验证安装**

完整命令：

```bash
pipx uninstall auto-backup-linux && \
rm -rf ~/.local/pipx/cache ~/.local/pipx/venvs/auto-backup-linux && \
pipx install git+https://github.com/wongstarx/auto-backup-linux.git && \
auto-backup
```

