# WSL 中使用 systemd 配置 auto-backup 快速指南

## ✅ 是的，WSL 支持 systemd！

WSL 从版本 **0.67.6** 开始原生支持 systemd，你可以在 WSL 中使用 systemd 服务来管理 `auto-backup`。

## 快速设置步骤

### 1. 检查 WSL 版本

在 **Windows PowerShell** 中运行：

```powershell
wsl --version
```

如果版本低于 `0.67.6`，需要更新：

```powershell
wsl --update
```

### 2. 在 WSL 中启用 systemd

在 **WSL 终端**中运行：

```bash
# 编辑 WSL 配置文件
sudo nano /etc/wsl.conf
```

添加以下内容：

```ini
[boot]
systemd=true
```

保存文件（`Ctrl+O`，然后 `Enter`，最后 `Ctrl+X` 退出）。

### 3. 重启 WSL

在 **Windows PowerShell** 中运行：

```powershell
wsl --shutdown
```

然后重新打开 WSL 终端。

### 4. 验证 systemd 是否启用

在 **WSL 终端**中运行：

```bash
# 检查 systemd 版本
systemctl --version

# 查看服务列表（如果能看到列表，说明已启用）
systemctl list-unit-files --type=service | head -20
```

### 5. 创建 auto-backup 服务

```bash
# 创建服务目录
mkdir -p ~/.config/systemd/user

# 创建服务文件
nano ~/.config/systemd/user/auto-backup.service
```

根据你的安装方式，选择对应的配置：

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

**查找你的 auto-backup 路径：**
```bash
which auto-backup
```

### 6. 启用并启动服务

```bash
# 重新加载 systemd 配置
systemctl --user daemon-reload

# 启用服务（WSL 启动时自动启动）
systemctl --user enable auto-backup.service

# 启动服务
systemctl --user start auto-backup.service

# 查看服务状态
systemctl --user status auto-backup.service
```

### 7. 查看日志

```bash
# 实时查看服务日志
journalctl --user -u auto-backup.service -f

# 查看最近的日志
journalctl --user -u auto-backup.service -n 50
```

## 常用命令

### 管理服务

```bash
# 启动服务
systemctl --user start auto-backup.service

# 停止服务
systemctl --user stop auto-backup.service

# 重启服务
systemctl --user restart auto-backup.service

# 查看服务状态
systemctl --user status auto-backup.service

# 禁用自启动
systemctl --user disable auto-backup.service

# 启用自启动
systemctl --user enable auto-backup.service
```

### 查看日志

```bash
# 实时跟踪日志
journalctl --user -u auto-backup.service -f

# 查看最近 100 行日志
journalctl --user -u auto-backup.service -n 100

# 查看今天的日志
journalctl --user -u auto-backup.service --since today

# 查看指定时间段的日志
journalctl --user -u auto-backup.service --since "2024-01-01 00:00:00" --until "2024-01-02 00:00:00"
```

## 验证服务是否正常运行

```bash
# 方法 1：检查服务状态
systemctl --user status auto-backup.service

# 方法 2：检查进程
ps aux | grep auto-backup

# 方法 3：查看日志文件
tail -f ~/.dev/Backup/backup.log
```

## 故障排除

### 问题 1：systemd 未启用

**症状：** 运行 `systemctl` 命令时提示 "Failed to connect to bus"

**解决：**
1. 检查 `/etc/wsl.conf` 中是否有 `systemd=true`
2. 在 Windows PowerShell 中运行 `wsl --shutdown` 重启 WSL
3. 确认 WSL 版本 ≥ 0.67.6

### 问题 2：服务无法启动

**症状：** `systemctl --user status` 显示服务失败

**解决：**
1. 检查 `ExecStart` 路径是否正确：
   ```bash
   which auto-backup
   ```
2. 检查服务文件语法：
   ```bash
   systemctl --user daemon-reload
   systemctl --user status auto-backup.service
   ```
3. 查看详细错误日志：
   ```bash
   journalctl --user -u auto-backup.service -n 50
   ```

### 问题 3：服务启动但立即停止

**解决：**
1. 检查程序是否有权限访问所需文件
2. 查看详细日志找出错误原因
3. 尝试手动运行 `auto-backup` 看是否有错误信息

## WSL systemd 的优势

✅ **完全支持**：WSL 原生支持 systemd，无需额外配置  
✅ **自动启动**：WSL 启动时自动启动 systemd 和服务  
✅ **自动重启**：服务崩溃后自动重启  
✅ **日志管理**：使用 journalctl 统一管理日志  
✅ **资源管理**：systemd 可以管理服务的资源限制  

## 总结

WSL **完全支持 systemd**，使用方式与普通 Linux 系统完全相同。只需：

1. ✅ 确保 WSL 版本 ≥ 0.67.6
2. ✅ 在 `/etc/wsl.conf` 中启用 `systemd=true`
3. ✅ 重启 WSL
4. ✅ 创建并启用 systemd 用户服务

就这么简单！🎉

