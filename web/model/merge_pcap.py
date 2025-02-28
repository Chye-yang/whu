from scapy.all import rdpcap, wrpcap
import os
from scapy.layers.inet import IP


def extract_unique_flows(pcap_file):
    unique_flows = set()
    packets = rdpcap(pcap_file)
    for packet in packets:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            # 将源IP和目的IP组合为元组，作为集合的元素
            flow = (src_ip, dst_ip)
            unique_flows.add(flow)
    return unique_flows


def merge_unique_flows(pcap_files, output_pcap):
    merged_flows = set()
    for pcap_file in pcap_files:
        unique_flows = extract_unique_flows(pcap_file)
        merged_flows.update(unique_flows)

    packets = []
    for pcap_file in pcap_files:
        packets.extend(rdpcap(pcap_file))

    # 筛选出不重复的流量记录
    filtered_packets = [packet for packet in packets if (packet[IP].src, packet[IP].dst) in merged_flows]

    # 写入新的.pcap文件
    wrpcap(output_pcap, filtered_packets)


# 获取文件夹下所有的.pcap文件
folder_path = '../data/000-all'  # 替换为你的.pcap文件所在的文件夹路径
pcap_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pcap')]

# 合并不重复的流量记录到新的.pcap文件
output_pcap = 'merged_unique_flows.pcap'  # 输出文件的名称
merge_unique_flows(pcap_files, output_pcap)