#!/bin/bash

# 定义要并行执行的次数
NUM_THREADS=30  # 根据需要设置线程数

# 定义网络接口
INTERFACE="eth1"

# 遍历当前目录下的所有.pcap文件
for pcap_file in ./*.pcap; do
    # 检查文件是否存在
    if [[ -f "$pcap_file" ]]; then
        echo "Starting tcpreplay for: $pcap_file..."
        tcpreplay -i "$INTERFACE" -p 2000 "$pcap_file" &  # 在后台执行tcpreplay命令
        sleep 0.1  # 可选：稍微延时，避免瞬间启动过多进程

        # 控制并行执行的线程数
        while (( $(jobs -r | wc -l) >= NUM_THREADS )); do
            sleep 1  # 等待，直到有可用的线程
        done
    else
        echo "No .pcap files found in the directory."
    fi
done

# 等待所有后台任务完成
wait

echo "All tcpreplay instances finished."
