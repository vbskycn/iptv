#!/bin/bash

LOCK_FILE="/tmp/syn_rclone.lock"
LOG_FILE="/tmp/syn_rclone.log"
MAX_LOG_AGE=3  # 最大记录保存天数

# 检查rclone命令是否存在
if ! command -v rclone &> /dev/null; then
    echo "rclone 命令未找到，请安装后再运行脚本."
    exit 1
fi

# 检查是否已有同名进程在运行
if [ -e "$LOCK_FILE" ]; then
    echo "rclone自动同步备份网站目录进程正在运行，程序自动退出，请结束后再次运行."
    exit 1
fi

# 创建锁文件
touch "$LOCK_FILE"

# 在脚本结束时删除锁文件
cleanup() {
    rm "$LOCK_FILE"
}
trap cleanup EXIT

while true; do
    # 获取当前时间戳
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # 运行同步命令，并将输出追加到日志文件
    /usr/bin/rclone sync --update --verbose /www/wwwroot/newavs.top one:/bt_backup/newavs.top >> "$LOG_FILE" 2>&1
    #/usr/bin/rclone sync --update --verbose /www/backup one:/bt_backup/armnew >> "$LOG_FILE" 2>&1	
    /usr/bin/rclone sync --update --verbose /www/wwwroot/newavs.top/wp-content/themes/puock/cache/ /opt/one/bt_backup/rclone_cache >> "$LOG_FILE" 2>&1
  
    # 删除 /opt/one/bt_backup/rclone_cache/ 下所有文件
    #rm -rf /opt/one/bt_backup/rclone_cache/*
	
    # 在日志行中添加同步时间戳
    echo "[$timestamp] Sync completed." >> "$LOG_FILE"

    # 删除超过最大保存天数的日志文件
    rm -f "$LOG_FILE"



    sleep 7200  # 每隔7200秒同步一次，可以根据需要进行调整
done
