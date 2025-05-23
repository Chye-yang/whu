import os
from scapy.all import *

def merge_pcap_files(output_filename="merged.pcap"):
    """
    查找当前目录下的所有 .pcap 文件并将它们合并。

    Args:
        output_filename (str): 合并后输出的文件名。
    """
    current_directory = '.'  # 表示当前目录
    pcap_files = []

    print("正在当前目录中搜索 .pcap 文件...")

    # 遍历当前目录下的所有文件
    for filename in os.listdir(current_directory):
        # 检查文件是否以 .pcap 结尾 (也包括 .pcapng 等常见格式)
        if filename.lower().endswith(('.pcap', '.pcapng', '.cap')):
            # 排除目标输出文件，避免重复读取
            if filename != output_filename:
                pcap_files.append(filename)
                print(f"  找到: {filename}")

    if not pcap_files:
        print("未在当前目录中找到任何 .pcap 文件。")
        return

    print(f"\n找到 {len(pcap_files)} 个 pcap 文件。开始合并...")

    all_packets = []
    file_count = 0

    # 逐一读取每个 pcap 文件
    for pcap_file in pcap_files:
        try:
            print(f"  正在读取: {pcap_file} ...")
            # 使用 rdpcap 读取数据包
            packets = rdpcap(pcap_file)
            all_packets.extend(packets)
            file_count += 1
        except Scapy_Exception as e:
            print(f"  读取文件 {pcap_file} 时出错: {e}")
        except Exception as e:
            print(f"  处理文件 {pcap_file} 时发生未知错误: {e}")

    if not all_packets:
        print("未能从任何文件中读取到数据包，无法创建合并文件。")
        return

    print(f"\n成功读取 {file_count} 个文件，共 {len(all_packets)} 个数据包。")
    print(f"正在将所有数据包写入到 {output_filename} ...")

    try:
        # 使用 wrpcap 将所有数据包写入新文件
        wrpcap(output_filename, all_packets)
        print(f"\n🎉 成功！所有 pcap 文件已合并到 {output_filename}")
    except Exception as e:
        print(f"\n写入 {output_filename} 时出错: {e}")

# --- 脚本主入口 ---
if __name__ == "__main__":
    merge_pcap_files()