# 项目结构说明

## 目录结构

```
linux/
├── auto_backup/              # 主包目录
│   ├── __init__.py          # 包初始化文件
│   ├── config.py            # 配置类
│   ├── manager.py           # 备份管理器类
│   └── cli.py               # 命令行接口
├── setup.py                 # 安装配置文件
├── requirements.txt         # 依赖列表
├── README.md               # 项目说明文档
├── LICENSE                 # 许可证文件
├── MANIFEST.in             # 清单文件
├── .gitignore              # Git忽略文件
├── PUBLISH.md              # 发布指南
├── STRUCTURE.md            # 本文件
└── example.py              # 使用示例

```

## 文件说明

### 核心文件

- **auto_backup/__init__.py**: 包入口，导出主要类和模块
- **auto_backup/config.py**: 备份配置类，包含所有可配置项
- **auto_backup/manager.py**: 备份管理器，实现备份、压缩、上传等核心功能
- **auto_backup/cli.py**: 命令行接口，提供定时备份功能

### 配置文件

- **setup.py**: Python包安装配置，定义包信息、依赖和入口点
- **requirements.txt**: Python依赖包列表
- **MANIFEST.in**: 指定打包时包含的文件

### 文档文件

- **README.md**: 项目主要文档，包含安装和使用说明
- **PUBLISH.md**: PyPI发布指南
- **STRUCTURE.md**: 项目结构说明（本文件）

### 其他文件

- **LICENSE**: MIT许可证
- **.gitignore**: Git版本控制忽略文件
- **example.py**: 使用示例代码

## 安装和使用

### 本地开发安装

```bash
cd linux
pip install -e .
```

### 从GitHub安装

```bash
pip install git+https://github.com/wongstarx/auto-backup-linux.git
```

### 使用命令行工具

```bash
auto-backup
```

### 在Python代码中使用

```python
from auto_backup import BackupManager

manager = BackupManager()
# ... 使用manager进行备份
```

## 发布流程

1. 更新版本号（setup.py）
2. 更新README.md中的更新日志
3. 构建包：`python -m build`
4. 上传到PyPI：`twine upload dist/*`

详细说明请参考 `PUBLISH.md`

