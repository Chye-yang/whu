import os
import sys
import csv
from scapy.all import PcapReader, TCP, UDP, IP, IPv6, ARP


HEADER = [
    "id","dur","proto","service","state","spkts","dpkts","sbytes","dbytes","rate",
    "sttl","dttl","sload","dload","sloss","dloss","sinpkt","dinpkt","sjit","djit",
    "swin","stcpb","dtcpb","dwin","tcprtt","synack","ackdat","smean","dmean",
    "trans_depth","response_body_len","ct_srv_src","ct_state_ttl","ct_dst_ltm",
    "ct_src_dport_ltm","ct_dst_sport_ltm","ct_dst_src_ltm","is_ftp_login","ct_ftp_cmd",
    "ct_flw_http_mthd","ct_src_ltm","ct_srv_dst","is_sm_ips_ports","attack_cat","label",
    "srcip","dstip"," port"
]


def infer_proto(pkt):
    if pkt.haslayer(ARP):
        return "arp"
    if pkt.haslayer(TCP):
        return "tcp"
    if pkt.haslayer(UDP):
        return "udp"
    return "other"


def get_ips_ports(pkt):
    src_ip = dst_ip = None
    sport = dport = None
    if pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
    elif pkt.haslayer(IPv6):
        src_ip = pkt[IPv6].src
        dst_ip = pkt[IPv6].dst
    if pkt.haslayer(TCP):
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
    elif pkt.haslayer(UDP):
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
    return src_ip, dst_ip, sport, dport


def main(pcap_path: str, out_csv: str):
    if not os.path.exists(pcap_path):
        print(f"pcap不存在: {pcap_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    flow_id = 0
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)

        with PcapReader(pcap_path) as pr:
            for pkt in pr:
                flow_id += 1

                proto = infer_proto(pkt)
                src_ip, dst_ip, sport, dport = get_ips_ports(pkt)

                # 近似映射：单包作为一条flow，字段对齐perflow.csv所需列
                dur = 0 if not hasattr(pkt, 'time') else 0
                spkts = 1
                dpkts = 0
                sbytes = len(pkt)
                dbytes = 0
                rate = 0
                sttl = pkt[IP].ttl if pkt.haslayer(IP) else 0
                dttl = 0
                sload = 0
                dload = 0
                sloss = 0
                dloss = 0
                sinpkt = 0
                dinpkt = 0
                sjit = 0
                djit = 0
                swin = 255
                stcpb = 0
                dtcpb = 0
                dwin = 255
                tcprtt = 0
                synack = 0
                ackdat = 0
                smean = sbytes
                dmean = dbytes
                trans_depth = 0
                response_body_len = 0
                ct_srv_src = 2
                ct_state_ttl = 2
                ct_dst_ltm = 1
                ct_src_dport_ltm = 1
                ct_dst_sport_ltm = 1
                ct_dst_src_ltm = 1
                is_ftp_login = 0
                ct_ftp_cmd = 0
                ct_flw_http_mthd = 0
                ct_src_ltm = 1
                ct_srv_dst = 1
                is_sm_ips_ports = 0
                attack_cat = "Normal_0"
                label = 0
                service = "-"
                state = "INT" if proto in ("udp", "tcp", "arp") else "-"

                # 端口列名为" port"，保留空格以与参考一致
                row = [
                    flow_id, dur, proto, service, state, spkts, dpkts, sbytes, dbytes, rate,
                    sttl, dttl, sload, dload, sloss, dloss, sinpkt, dinpkt, sjit, djit,
                    swin, stcpb, dtcpb, dwin, tcprtt, synack, ackdat, smean, dmean,
                    trans_depth, response_body_len, ct_srv_src, ct_state_ttl, ct_dst_ltm,
                    ct_src_dport_ltm, ct_dst_sport_ltm, ct_dst_src_ltm, is_ftp_login,
                    ct_ftp_cmd, ct_flw_http_mthd, ct_src_ltm, ct_srv_dst, is_sm_ips_ports,
                    attack_cat, label, src_ip or "", dst_ip or "", dport or sport or 0
                ]

                writer.writerow(row)

    print(f"已生成: {out_csv}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python pcap_to_perflow_beijing.py <pcap_path> <out_csv>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])


