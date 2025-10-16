#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PCAP文件转换为PerFlow格式的脚本
将pcap包文件转换为网络流分析CSV格式
"""

import os
import sys
import csv
import time
from collections import defaultdict, Counter
from datetime import datetime
import ipaddress

try:
    from scapy.all import *
    import pandas as pd
except ImportError as e:
    print(f"缺少必要的包: {e}")
    print("请安装: pip install scapy pandas")
    sys.exit(1)


class FlowAnalyzer:
    """网络流分析器"""
    
    def __init__(self):
        self.flows = defaultdict(lambda: {
            'packets': [],
            'start_time': None,
            'end_time': None,
            'src_ip': None,
            'dst_ip': None,
            'src_port': None,
            'dst_port': None,
            'protocol': None,
            'src_bytes': 0,
            'dst_bytes': 0,
            'src_packets': 0,
            'dst_packets': 0,
            'src_ttl': [],
            'dst_ttl': [],
            'flags': [],
            'window_sizes': [],
            'payload_lengths': []
        })
        
    def get_flow_key(self, packet):
        """生成流的唯一标识符"""
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet[IP].proto
            
            # 获取端口信息
            src_port = 0
            dst_port = 0
            
            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
            elif packet.haslayer(ICMP):
                src_port = packet[ICMP].type
                dst_port = packet[ICMP].code
            
            # 创建双向流的统一标识符
            if src_ip < dst_ip or (src_ip == dst_ip and src_port < dst_port):
                return f"{src_ip}:{src_port}-{dst_ip}:{dst_port}-{protocol}"
            else:
                return f"{dst_ip}:{dst_port}-{src_ip}:{src_port}-{protocol}"
        
        return None
    
    def analyze_packet(self, packet):
        """分析单个数据包"""
        flow_key = self.get_flow_key(packet)
        if not flow_key:
            return
            
        flow = self.flows[flow_key]
        timestamp = packet.time
        
        # 初始化流信息
        if flow['start_time'] is None:
            flow['start_time'] = timestamp
            if packet.haslayer(IP):
                flow['src_ip'] = packet[IP].src
                flow['dst_ip'] = packet[IP].dst
                flow['protocol'] = packet[IP].proto
                
                if packet.haslayer(TCP):
                    flow['src_port'] = packet[TCP].sport
                    flow['dst_port'] = packet[TCP].dport
                elif packet.haslayer(UDP):
                    flow['src_port'] = packet[UDP].sport
                    flow['dst_port'] = packet[UDP].dport
                elif packet.haslayer(ICMP):
                    flow['src_port'] = packet[ICMP].type
                    flow['dst_port'] = packet[ICMP].code
        
        flow['end_time'] = timestamp
        flow['packets'].append(packet)
        
        # 统计字节数和包数
        if packet.haslayer(IP):
            packet_size = len(packet)
            flow['src_bytes'] += packet_size
            flow['src_packets'] += 1
            
            # 记录TTL
            flow['src_ttl'].append(packet[IP].ttl)
            
            # 记录TCP标志
            if packet.haslayer(TCP):
                flow['flags'].append(packet[TCP].flags)
                flow['window_sizes'].append(packet[TCP].window)
            
            # 记录载荷长度
            if packet.haslayer(Raw):
                flow['payload_lengths'].append(len(packet[Raw].load))
    
    def calculate_flow_features(self, flow_key, flow_data):
        """计算流的特征"""
        duration = flow_data['end_time'] - flow_data['start_time']
        total_packets = flow_data['src_packets']
        total_bytes = flow_data['src_bytes']
        
        # 计算速率
        rate = total_bytes / duration if duration > 0 else 0
        
        # 计算平均TTL
        avg_ttl = sum(flow_data['src_ttl']) / len(flow_data['src_ttl']) if flow_data['src_ttl'] else 0
        
        # 计算平均包间隔
        if len(flow_data['packets']) > 1:
            intervals = []
            for i in range(1, len(flow_data['packets'])):
                intervals.append(flow_data['packets'][i].time - flow_data['packets'][i-1].time)
            avg_interval = sum(intervals) / len(intervals) if intervals else 0
        else:
            avg_interval = 0
        
        # 确定协议名称
        protocol_map = {1: 'icmp', 6: 'tcp', 17: 'udp'}
        protocol_name = protocol_map.get(flow_data['protocol'], 'unknown')
        
        # 确定服务类型（基于端口）
        service = '-'
        if flow_data['src_port']:
            port = flow_data['src_port']
            if port in [80, 8080]: service = 'http'
            elif port in [443]: service = 'https'
            elif port in [21]: service = 'ftp'
            elif port in [22]: service = 'ssh'
            elif port in [23]: service = 'telnet'
            elif port in [25]: service = 'smtp'
            elif port in [53]: service = 'dns'
            elif port in [110]: service = 'pop3'
            elif port in [143]: service = 'imap'
        
        # 确定连接状态
        state = 'INT'  # 默认状态
        if flow_data['flags']:
            flags = set(flow_data['flags'])
            if 2 in flags and 18 in flags:  # SYN + ACK
                state = 'EST'
            elif 1 in flags:  # FIN
                state = 'FIN'
            elif 4 in flags:  # RST
                state = 'RST'
        
        return {
            'id': hash(flow_key) % 1000000,  # 生成ID
            'dur': duration,
            'proto': protocol_name,
            'service': service,
            'state': state,
            'spkts': total_packets,
            'dpkts': 0,  # 简化处理
            'sbytes': total_bytes,
            'dbytes': 0,  # 简化处理
            'rate': rate,
            'sttl': int(avg_ttl),
            'dttl': 0,  # 简化处理
            'sload': rate,
            'dload': 0,  # 简化处理
            'sloss': 0,  # 简化处理
            'dloss': 0,  # 简化处理
            'sinpkt': avg_interval,
            'dinpkt': 0,  # 简化处理
            'sjit': 0,  # 简化处理
            'djit': 0,  # 简化处理
            'swin': sum(flow_data['window_sizes']) / len(flow_data['window_sizes']) if flow_data['window_sizes'] else 0,
            'stcpb': 0,  # 简化处理
            'dtcpb': 0,  # 简化处理
            'dwin': 0,  # 简化处理
            'tcprtt': 0,  # 简化处理
            'synack': 0,  # 简化处理
            'ackdat': 0,  # 简化处理
            'smean': total_bytes / total_packets if total_packets > 0 else 0,
            'dmean': 0,  # 简化处理
            'trans_depth': 0,  # 简化处理
            'response_body_len': 0,  # 简化处理
            'ct_srv_src': 0,  # 简化处理
            'ct_state_ttl': 0,  # 简化处理
            'ct_dst_ltm': 0,  # 简化处理
            'ct_src_dport_ltm': 0,  # 简化处理
            'ct_dst_sport_ltm': 0,  # 简化处理
            'ct_dst_src_ltm': 0,  # 简化处理
            'is_ftp_login': 0,  # 简化处理
            'ct_ftp_cmd': 0,  # 简化处理
            'ct_flw_http_mthd': 0,  # 简化处理
            'ct_src_ltm': 0,  # 简化处理
            'ct_srv_dst': 0,  # 简化处理
            'is_sm_ips_ports': 0,  # 简化处理
            'attack_cat': 'Normal_0',  # 默认正常
            'label': 0,  # 默认正常
            'srcip': flow_data['src_ip'],
            'dstip': flow_data['dst_ip'],
            'port': flow_data['src_port']
        }


def pcap_to_perflow(pcap_file, output_file):
    """将PCAP文件转换为PerFlow格式"""
    print(f"开始处理PCAP文件: {pcap_file}")
    
    # 检查文件是否存在
    if not os.path.exists(pcap_file):
        print(f"错误: PCAP文件不存在: {pcap_file}")
        return False
    
    # 创建流分析器
    analyzer = FlowAnalyzer()
    
    try:
        # 读取PCAP文件
        print("正在读取PCAP文件...")
        packets = rdpcap(pcap_file)
        print(f"读取到 {len(packets)} 个数据包")
        
        # 分析每个数据包
        print("正在分析数据包...")
        for i, packet in enumerate(packets):
            if i % 1000 == 0:
                print(f"已处理 {i}/{len(packets)} 个数据包")
            analyzer.analyze_packet(packet)
        
        print(f"识别到 {len(analyzer.flows)} 个网络流")
        
        # 生成CSV文件
        print("正在生成CSV文件...")
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes',
                'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt',
                'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat',
                'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl',
                'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
                'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst',
                'is_sm_ips_ports', 'attack_cat', 'label', 'srcip', 'dstip', 'port'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # 写入流数据
            for flow_key, flow_data in analyzer.flows.items():
                features = analyzer.calculate_flow_features(flow_key, flow_data)
                writer.writerow(features)
        
        print(f"转换完成! 输出文件: {output_file}")
        return True
        
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        return False


def main():
    """主函数"""
    # 输入和输出文件路径
    pcap_file = "/home/whu/os/Data/OriginPcap/second/ceshi_815.pcap"
    output_file = "/home/whu/os/Data/analysis/perflow_beijing2-2.csv"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 执行转换
    success = pcap_to_perflow(pcap_file, output_file)
    
    if success:
        print("脚本执行成功!")
    else:
        print("脚本执行失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()
