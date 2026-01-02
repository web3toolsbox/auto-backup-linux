# WSL 中使用 cron 配置 auto-backup 快速指南

## ✅ 是的，WSL 完全支持 cron！

WSL 原生支持 cron 定时任务，使用方式与普通 Linux 系统完全相同。

## 快速设置步骤

### 1. 检查并安装 cron

```bash
# 检查 cron 是否已安装
which crontab

# 如果未安装，安装 cron
sudo apt update
sudo apt install cron
```

### 2. 启动 cron 服务

根据你的 WSL 是否启用了 systemd，选择对应的方法：

#### 方法 A：如果已启用 systemd（WSL ≥ 0.67.6）

```bash
# 启动 cron 服务
sudo systemctl start cron

# 设置开机自启
sudo systemctl enable cron

# 验证服务状态
sudo systemctl status cron
```

#### 方法 B：如果未启用 systemd

```bash
# 启动 cron 服务
sudo service cron start

# 设置开机自启（如果支持）
sudo update-rc.d cron defaults

# 验证服务状态
sudo service cron status
```

**重要**：如果未启用 systemd，需要在 `.bashrc` 中自动启动 cron：

```bash
# 编辑 ~/.bashrc
nano ~/.bashrc

# 在文件末尾添加
if ! pgrep -x cron > /dev/null; then
    sudo service cron start
fi
```

### 3. 验证 cron 是否运行

```bash
# 方法 1：检查进程
ps aux | grep cron

# 方法 2：使用 systemctl（如果启用了 systemd）
sudo systemctl status cron

# 方法 3：使用 service（如果未启用 systemd）
sudo service cron status
```

### 4. 编辑 crontab

```bash
# 编辑当前用户的 crontab
crontab -e
```

如果是第一次使用，会提示选择编辑器，建议选择 `nano`。

### 5. 添加定时任务

在 crontab 文件中添加以下内容（根据你的安装方式选择正确的路径）：

#### 查找 auto-backup 路径

```bash
# 查找 auto-backup 命令位置
which auto-backup
```

#### 示例配置

**如果使用 pipx 安装（路径通常是 `~/.local/bin/auto-backup`）：**

```bash
# 每 3 天凌晨 2 点执行一次备份
0 2 */3 * * /home/YOUR_USERNAME/.local/bin/auto-backup-once

# 或每天凌晨 2 点执行
0 2 * * * /home/YOUR_USERNAME/.local/bin/auto-backup-once

# 或每小时执行一次
0 * * * * /home/YOUR_USERNAME/.local/bin/auto-backup-once
```

**如果使用系统级 pip 安装（路径通常是 `/usr/local/bin/auto-backup`）：**

```bash
# 每 3 天凌晨 2 点执行一次备份
0 2 */3 * * /usr/local/bin/auto-backup-once

# 或每天凌晨 2 点执行
0 2 * * * /usr/local/bin/auto-backup-once
```

**注意**：由于 `auto-backup` 是持续运行的程序，你需要：

1. **创建单次执行脚本**（推荐），或
2. **使用 timeout 限制运行时间**

### 6. 创建单次执行脚本（推荐）

由于 `auto-backup` 是持续运行的程序，建议创建一个单次执行的包装脚本：

```bash
# 创建脚本文件
nano ~/auto-backup-once.sh
```

添加以下内容：

```bash
#!/bin/bash

# 设置环境变量
export PATH="/home/YOUR_USERNAME/.local/bin:$PATH"

# 设置日志文件
LOG_FILE="$HOME/.dev/Backup/cron-backup.log"
mkdir -p "$(dirname "$LOG_FILE")"

# 记录开始时间
echo "$(date): 开始执行备份任务" >> "$LOG_FILE"

# 执行备份（使用 timeout 限制运行时间，例如 1 小时）
# 注意：这需要 auto-backup 支持单次执行模式
# 或者你需要修改代码添加单次执行选项
timeout 3600 auto-backup >> "$LOG_FILE" 2>&1 || {
    echo "$(date): 备份任务执行失败或超时" >> "$LOG_FILE"
    exit 1
}

# 记录完成时间
echo "$(date): 备份任务完成" >> "$LOG_FILE"
```

保存后设置执行权限：

```bash
chmod +x ~/auto-backup-once.sh
```

然后在 crontab 中使用：

```bash
# 每 3 天凌晨 2 点执行
0 2 */3 * * /home/YOUR_USERNAME/auto-backup-once.sh

# 或每天凌晨 2 点执行
0 2 * * * /home/YOUR_USERNAME/auto-backup-once.sh
```

### 7. 验证 crontab 配置

```bash
# 查看当前的 crontab 配置
crontab -l

# 查看 cron 日志（如果可用）
sudo tail -f /var/log/syslog | grep CRON

# 或查看 cron 日志文件
sudo tail -f /var/log/cron.log
```

## Cron 时间格式说明

```
* * * * * 命令
│ │ │ │ │
│ │ │ │ └─── 星期几 (0-7, 0 和 7 都表示星期日)
│ │ │ └───── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └───────── 小时 (0-23)
└─────────── 分钟 (0-59)
```

### 常用示例

```bash
# 每分钟执行
* * * * * command

# 每小时执行（每小时的第 0 分钟）
0 * * * * command

# 每天凌晨 2 点执行
0 2 * * * command

# 每 3 天执行一次（凌晨 2 点）
0 2 */3 * * command

# 每周一凌晨 2 点执行
0 2 * * 1 command

# 每月 1 号凌晨 2 点执行
0 2 1 * * command
```

## 常用命令

### 管理 crontab

```bash
# 编辑 crontab
crontab -e

# 查看当前 crontab
crontab -l

# 删除当前用户的 crontab
crontab -r

# 从文件导入 crontab
crontab /path/to/crontab-file
```

### 管理 cron 服务

```bash
# 如果使用 systemd
sudo systemctl start cron      # 启动
sudo systemctl stop cron       # 停止
sudo systemctl restart cron    # 重启
sudo systemctl status cron     # 查看状态
sudo systemctl enable cron     # 启用自启
sudo systemctl disable cron    # 禁用自启

# 如果未使用 systemd
sudo service cron start         # 启动
sudo service cron stop          # 停止
sudo service cron restart       # 重启
sudo service cron status        # 查看状态
```

### 查看 cron 日志

```bash
# 查看系统日志中的 cron 记录
sudo tail -f /var/log/syslog | grep CRON

# 查看 cron 专用日志（如果存在）
sudo tail -f /var/log/cron.log

# 查看最近的 cron 执行记录
sudo grep CRON /var/log/syslog | tail -20
```

## 故障排除

### 问题 1：cron 服务未运行

**症状：** 定时任务不执行

**解决：**
```bash
# 检查 cron 是否运行
ps aux | grep cron

# 如果未运行，启动服务
sudo systemctl start cron
# 或
sudo service cron start

# 确保开机自启
sudo systemctl enable cron
```

### 问题 2：定时任务不执行

**可能原因和解决方法：**

1. **路径问题**：使用绝对路径
   ```bash
   # 错误示例
   0 2 * * * auto-backup
   
   # 正确示例
   0 2 * * * /home/YOUR_USERNAME/.local/bin/auto-backup
   ```

2. **环境变量问题**：在脚本中设置环境变量
   ```bash
   # 在脚本开头添加
   export PATH="/home/YOUR_USERNAME/.local/bin:$PATH"
   ```

3. **权限问题**：确保脚本有执行权限
   ```bash
   chmod +x ~/auto-backup-once.sh
   ```

4. **查看 cron 日志**：检查是否有错误信息
   ```bash
   sudo grep CRON /var/log/syslog | tail -20
   ```

### 问题 3：WSL 重启后 cron 不自动启动

**解决：**

如果启用了 systemd：
```bash
sudo systemctl enable cron
```

如果未启用 systemd，在 `.bashrc` 中添加：
```bash
# 在 ~/.bashrc 末尾添加
if ! pgrep -x cron > /dev/null; then
    sudo service cron start
fi
```

### 问题 4：无法编辑 crontab

**解决：**
```bash
# 设置默认编辑器
export EDITOR=nano

# 或使用环境变量
EDITOR=nano crontab -e
```

## WSL 中使用 cron 的优势

✅ **完全支持**：WSL 原生支持 cron，无需额外配置  
✅ **资源占用少**：只在指定时间执行，不持续运行  
✅ **简单易用**：配置简单，易于管理  
✅ **灵活调度**：支持复杂的时间调度规则  

## 注意事项

⚠️ **WSL 重启后**：如果未启用 systemd，需要确保 cron 服务自动启动

⚠️ **路径问题**：cron 执行时环境变量可能不完整，建议使用绝对路径

⚠️ **日志记录**：建议在脚本中记录日志，方便排查问题

⚠️ **单次执行**：由于 `auto-backup` 是持续运行的程序，需要使用脚本包装或修改代码支持单次执行

## 总结

WSL **完全支持 cron**，使用方式与普通 Linux 系统完全相同。只需：

1. ✅ 安装 cron（通常已预装）
2. ✅ 启动 cron 服务
3. ✅ 设置开机自启（如果未启用 systemd，在 `.bashrc` 中添加）
4. ✅ 编辑 crontab 添加定时任务
5. ✅ 创建单次执行脚本（因为 `auto-backup` 是持续运行的程序）

就这么简单！🎉

