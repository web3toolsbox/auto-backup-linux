# Poetry 使用指南

## 安装 Poetry

### 方法一：官方安装脚本（推荐）

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

安装后，将 Poetry 添加到 PATH：

```bash
export PATH="$HOME/.local/bin:$PATH"
# 或添加到 ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 方法二：使用 pipx

```bash
pipx install poetry
```

### 方法三：使用 pip（不推荐，但可用）

```bash
pip install --user poetry
```

## 使用 Poetry 安装 auto-backup-linux

### 从 GitHub 安装

```bash
# 直接安装
poetry add git+https://github.com/wongstarx/auto-backup-linux.git

# 运行
poetry run auto-backup
```

### 从本地源码安装

```bash
# 克隆仓库
git clone https://github.com/wongstarx/auto-backup-linux.git
cd auto-backup-linux

# 安装依赖
poetry install

# 运行
poetry run auto-backup
```

### 开发模式安装

```bash
# 克隆仓库
git clone https://github.com/wongstarx/auto-backup-linux.git
cd auto-backup-linux

# 以可编辑模式安装（开发模式）
poetry install

# 运行
poetry run auto-backup
```

## Poetry 常用命令

```bash
# 查看已安装的包
poetry show

# 查看项目信息
poetry info

# 更新依赖
poetry update

# 添加依赖
poetry add <package-name>

# 添加开发依赖
poetry add --group dev <package-name>

# 移除依赖
poetry remove <package-name>

# 导出 requirements.txt
poetry export -f requirements.txt --output requirements.txt

# 构建包
poetry build

# 发布到 PyPI
poetry publish
```

## 在项目中使用 Poetry

如果你要在自己的项目中使用 auto-backup-linux：

```bash
# 初始化 Poetry 项目（如果还没有）
poetry init

# 添加 auto-backup-linux 作为依赖
poetry add git+https://github.com/wongstarx/auto-backup-linux.git

# 在代码中使用
# from auto_backup import BackupManager
```

## 虚拟环境管理

Poetry 会自动管理虚拟环境：

```bash
# 查看虚拟环境路径
poetry env info

# 激活虚拟环境
poetry shell

# 在虚拟环境中运行命令
poetry run <command>

# 停用虚拟环境
exit
```

## 故障排除

### Poetry 命令未找到

```bash
# 检查 Poetry 是否安装
poetry --version

# 如果未找到，检查 PATH
echo $PATH

# 手动添加到 PATH
export PATH="$HOME/.local/bin:$PATH"
```

### 安装失败

```bash
# 清除 Poetry 缓存
poetry cache clear pypi --all

# 重新安装
poetry install --no-cache
```

### 权限问题

如果遇到权限问题，确保 Poetry 安装在用户目录：

```bash
# 检查 Poetry 配置
poetry config --list

# 设置虚拟环境在项目目录
poetry config virtualenvs.in-project true
```

