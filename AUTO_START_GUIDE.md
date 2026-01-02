# Auto Backup Linux 自启动配置指南

## 概述

`auto-backup` 是一个持续运行的程序（包含 `while True` 循环），需要选择合适的自启动方式。

## ⚠️ 重要提示

**不推荐**直接在 `.bashrc` 中启动，因为：
1. `.bashrc` 只在交互式 shell 启动时执行
2. 程序会阻塞终端（需要后台运行）
3. 系统重启后不会自动启动

## 推荐方案

### 方案一：使用 systemd 用户服务（⭐ 最推荐）

这是最可靠的方式，支持开机自启、自动重启、日志管理。

#### ⚠️ WSL 用户注意

**WSL 支持 systemd，但需要先启用！**

WSL 从版本 0.67.6 开始支持 systemd。如果你的 WSL 版本较旧，需要先更新：

```powershell
# 在 Windows PowerShell 中检查 WSL 版本
wsl --version

# 如果版本低于 0.67.6，更新 WSL
wsl --update
```

**在 WSL 中启用 systemd：**

1. 编辑或创建 `/etc/wsl.conf` 文件：
```bash
sudo nano /etc/wsl.conf
```

2. 添加以下内容：
```ini
[boot]
systemd=true
```

3. 保存文件后，在 Windows PowerShell 中重启 WSL：
```powershell
wsl --shutdown
```

4. 重新启动 WSL 后，验证 systemd 是否启用：
```bash
systemctl list-unit-files --type=service
```

如果能看到服务列表，说明 systemd 已成功启用，可以继续下面的步骤。

#### 步骤 1：创建服务文件

```bash
# 创建服务文件
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/auto-backup.service
```

#### 步骤 2：编辑服务文件内容

根据你的安装方式选择对应的 `ExecStart` 路径：

**如果使用 pipx 安装：**
```ini
[Unit]
Description=Auto Backup Linux Service
After=network.target

[Service]
Type=simple
ExecStart=/home/YOUR_USERNAME/.local/bin/auto-backup
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**如果使用系统级 pip 安装：**
```ini
[Unit]
Description=Auto Backup Linux Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/auto-backup
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**如果使用虚拟环境：**
```ini
[Unit]
Description=Auto Backup Linux Service
After=network.target

[Service]
Type=simple
ExecStart=/path/to/venv/bin/auto-backup
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

#### 步骤 3：启用并启动服务

```bash
# 重新加载 systemd 配置
systemctl --user daemon-reload

# 启用服务（开机自启）
systemctl --user enable auto-backup.service

# 启动服务
systemctl --user start auto-backup.service

# 查看服务状态
systemctl --user status auto-backup.service

# 查看日志
journalctl --user -u auto-backup.service -f
```

#### 步骤 4：设置用户服务在系统启动时运行（可选）

**对于普通 Linux 系统：**
```bash
# 启用用户服务在系统启动时运行
sudo loginctl enable-linger $USER
```

**对于 WSL：**
WSL 中通常不需要 `enable-linger`，因为 WSL 启动时会自动启动 systemd。但如果你遇到问题，可以尝试：
```bash
# 在 WSL 中启用 linger（如果支持）
sudo loginctl enable-linger $USER
```

### 方案二：使用 cron 定时任务

如果不需要持续运行，可以使用 cron 定时执行。

#### ⚠️ WSL 用户注意

**WSL 完全支持 cron！** 但需要确保 cron 服务正在运行。

**在 WSL 中启用 cron：**

1. 检查 cron 是否已安装：
```bash
which crontab
# 如果未安装，安装 cron：
sudo apt update
sudo apt install cron
```

2. 启动 cron 服务：
```bash
# 如果使用 systemd（WSL ≥ 0.67.6）
sudo systemctl start cron
sudo systemctl enable cron

# 如果未启用 systemd，使用传统方式
sudo service cron start
```

3. 验证 cron 是否运行：
```bash
# 检查 cron 进程
ps aux | grep cron

# 或使用 systemctl（如果启用了 systemd）
sudo systemctl status cron
```

4. **重要**：如果 WSL 未启用 systemd，需要在 `.bashrc` 中自动启动 cron：
```bash
# 在 ~/.bashrc 末尾添加
if ! pgrep -x cron > /dev/null; then
    sudo service cron start
fi
```

#### 步骤 1：编辑 crontab

```bash
crontab -e
```

#### 步骤 2：添加定时任务

根据你的安装方式，使用正确的路径：

**如果使用 pipx 安装：**
```bash
# 每 3 天执行一次备份（根据 BACKUP_INTERVAL 配置）
0 2 */3 * * /home/YOUR_USERNAME/.local/bin/auto-backup-once

# 或每天凌晨 2 点检查并执行备份
0 2 * * * /home/YOUR_USERNAME/.local/bin/auto-backup-once
```

**如果使用系统级 pip 安装：**
```bash
# 每 3 天执行一次备份
0 2 */3 * * /usr/local/bin/auto-backup-once

# 或每天凌晨 2 点检查并执行备份
0 2 * * * /usr/local/bin/auto-backup-once
```

**注意**：需要创建一个只执行一次备份的脚本，因为默认的 `auto-backup` 是持续运行的。

#### 创建单次执行脚本（可选）

如果需要使用 cron，可以创建一个只执行一次备份的脚本：

```bash
# 创建脚本
nano ~/auto-backup-once.sh
```

添加内容：
```bash
#!/bin/bash
# 单次备份脚本

# 设置环境变量（如果需要）
export PATH="/home/YOUR_USERNAME/.local/bin:$PATH"

# 执行一次备份（需要修改 auto-backup 代码支持单次执行）
# 或者使用 timeout 限制运行时间
timeout 3600 auto-backup || true
```

保存后设置执行权限：
```bash
chmod +x ~/auto-backup-once.sh
```

然后在 crontab 中使用：
```bash
0 2 */3 * * /home/YOUR_USERNAME/auto-backup-once.sh
```

### 方案三：在 `.bashrc` 中后台启动（不推荐）

如果必须使用 `.bashrc`，可以这样配置：

```bash
# 在 ~/.bashrc 末尾添加
# 检查 auto-backup 是否已在运行
if ! pgrep -f "auto-backup" > /dev/null; then
    # 使用 nohup 在后台运行，并重定向输出
    nohup auto-backup > ~/.auto-backup.log 2>&1 &
    echo "Auto-backup started in background (PID: $!)"
fi
```

**缺点**：
- 只在交互式登录时执行
- 进程可能不稳定
- 系统重启后不会自动启动

### 方案四：使用 screen 或 tmux

```bash
# 使用 screen
screen -dmS auto-backup auto-backup

# 或使用 tmux
tmux new-session -d -s auto-backup 'auto-backup'
```

## 查找 auto-backup 可执行文件路径

如果不知道 `auto-backup` 的安装路径，可以使用以下命令查找：

```bash
# 查找 auto-backup 命令位置
which auto-backup

# 或使用
whereis auto-backup

# 或使用
find ~ -name "auto-backup" -type f 2>/dev/null
```

## 验证服务运行

```bash
# 检查进程是否运行
ps aux | grep auto-backup

# 查看日志文件
tail -f ~/.dev/Backup/backup.log

# 如果使用 systemd，查看服务日志
journalctl --user -u auto-backup.service -f
```

## 停止服务

### systemd 方式
```bash
systemctl --user stop auto-backup.service
systemctl --user disable auto-backup.service
```

### 其他方式
```bash
# 查找并终止进程
pkill -f auto-backup

# 或使用
killall auto-backup
```

## WSL 特殊说明

### WSL 中 systemd 的支持情况

✅ **WSL 支持 systemd**（WSL 版本 ≥ 0.67.6）

WSL 从版本 0.67.6 开始原生支持 systemd，这意味着：
- ✅ 可以在 WSL 中使用 `systemctl` 命令
- ✅ 可以使用 systemd 用户服务
- ✅ 支持服务自启动（WSL 启动时自动启动）
- ✅ 支持服务自动重启

### WSL 启用 systemd 的完整步骤

1. **检查 WSL 版本**（在 Windows PowerShell 中）：
```powershell
wsl --version
```

2. **更新 WSL**（如果版本低于 0.67.6）：
```powershell
wsl --update
```

3. **在 WSL 中配置 systemd**：
```bash
# 编辑配置文件
sudo nano /etc/wsl.conf
```

添加内容：
```ini
[boot]
systemd=true
```

4. **重启 WSL**（在 Windows PowerShell 中）：
```powershell
wsl --shutdown
```

5. **重新打开 WSL 并验证**：
```bash
# 验证 systemd 是否运行
systemctl --version

# 查看服务列表
systemctl list-unit-files --type=service
```

### WSL 中的注意事项

- WSL 重启后，systemd 会自动启动
- 如果 Windows 休眠或重启，WSL 中的服务也会自动恢复
- 可以使用 `systemctl --user` 管理用户服务，无需 root 权限
- 日志查看方式与普通 Linux 相同：`journalctl --user -u auto-backup.service`

## 总结

| 方案 | 优点 | 缺点 | 推荐度 | WSL 支持 |
|------|------|------|--------|----------|
| systemd 用户服务 | 稳定、自动重启、开机自启 | 需要 systemd（WSL ≥ 0.67.6） | ⭐⭐⭐⭐⭐ | ✅ 完全支持 |
| cron 定时任务 | 简单、资源占用少 | 需要修改代码支持单次执行，WSL 需确保 cron 服务运行 | ⭐⭐⭐⭐ | ✅ 完全支持 |
| .bashrc 后台启动 | 简单 | 不稳定、不持久 | ⭐⭐ | ✅ 支持 |
| screen/tmux | 简单 | 需要手动管理 | ⭐⭐⭐ | ✅ 支持 |

**强烈推荐使用 systemd 用户服务**，这是最可靠和专业的方案。**WSL 完全支持 systemd**，只需确保 WSL 版本 ≥ 0.67.6 并在 `/etc/wsl.conf` 中启用即可。

