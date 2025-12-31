# 修复 ModuleNotFoundError 问题

## 问题原因

之前的包结构不正确：
- 文件（`cli.py`, `config.py`, `manager.py`, `__init__.py`）都在根目录
- 但 `setup.py` 中的入口点配置是 `auto_backup.cli:main`
- `find_packages()` 找不到 `auto_backup` 包，导致安装后无法导入

## 已修复

✅ 已将文件移动到正确的包目录：
```
auto_backup/
├── __init__.py
├── cli.py
├── config.py
└── manager.py
```

✅ 已更新 `pyproject.toml` 中的入口点配置

## 如何应用修复

### 1. 提交更改到 GitHub

```bash
cd /path/to/auto-backup-linux
git add auto_backup/ pyproject.toml
git commit -m "Fix: Move files to auto_backup package directory"
git push
```

### 2. 重新安装包

```bash
# 卸载旧版本
pipx uninstall auto-backup-linux

# 重新安装
pipx install git+https://github.com/wongstarx/auto-backup-linux.git

# 测试
auto-backup
```

### 3. 如果仍有问题

```bash
# 清除 pipx 缓存
pipx uninstall auto-backup-linux
pipx cache clear

# 重新安装
pipx install --force git+https://github.com/wongstarx/auto-backup-linux.git
```

## 验证安装

```bash
# 检查包是否正确安装
pipx list

# 检查入口点
which auto-backup

# 运行命令
auto-backup
```

## 当前包结构

```
auto-backup-linux/
├── auto_backup/          # 主包目录
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   └── manager.py
├── setup.py
├── pyproject.toml
├── README.md
└── ...
```

现在包结构符合 Python 标准，应该可以正常工作了！

