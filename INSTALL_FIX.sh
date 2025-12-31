#!/bin/bash
# 修复安装问题的脚本

echo "🔍 检查当前安装状态..."
pipx list | grep auto-backup || echo "未安装"

echo ""
echo "🗑️  卸载旧版本..."
pipx uninstall auto-backup-linux 2>/dev/null || true

echo ""
echo "🧹 清除 pipx 缓存..."
rm -rf ~/.local/pipx/cache 2>/dev/null || true
rm -rf ~/.local/pipx/venvs/auto-backup-linux 2>/dev/null || true

echo ""
echo "📦 重新安装..."
pipx install git+https://github.com/wongstarx/auto-backup-linux.git

echo ""
echo "✅ 验证安装..."
echo "检查版本:"
pipx list | grep auto-backup

echo ""
echo "检查包结构:"
~/.local/pipx/venvs/auto-backup-linux/bin/python -c "import sys; import os; site_packages = [p for p in sys.path if 'site-packages' in p][0]; print('Site packages:', site_packages); print('Auto_backup exists:', os.path.exists(os.path.join(site_packages, 'auto_backup')))" 2>/dev/null || echo "无法检查"

echo ""
echo "测试导入:"
~/.local/pipx/venvs/auto-backup-linux/bin/python -c "import auto_backup; print('✅ 导入成功! 版本:', auto_backup.__version__)" 2>&1 || echo "❌ 导入失败"

echo ""
echo "运行命令:"
auto-backup --help 2>&1 | head -5 || echo "❌ 命令执行失败"

