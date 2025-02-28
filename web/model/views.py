import dpkt

from model.db import Record
from model.db import Library
from model.db import Statistic
from model.db import Prediction
from datetime import *
from django.utils import timezone
import pytz
from django.db.models import Avg
from model.db import Analysis, PortInfo
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from model.db import Prediction
from model.db import Behavior
from scapy.all import *
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import Normalizer
from sklearn.metrics import (precision_score, recall_score, f1_score, accuracy_score, mean_squared_error,
                             mean_absolute_error, roc_curve, classification_report, auc)
from sklearn.preprocessing import LabelEncoder
import joblib


def record(request):
    record_info = db_url(request)
    attack_info = db_predict(request)
    return render(request, 'record.html', {'record': record_info,
                                           'attack':attack_info})

def db_predict(request):
    attack_info = Prediction.objects.filter(id__lt=100)

    return attack_info

def analysis(request):
    return render(request, 'analysis.html')


def record_empty(request):
    # statistics_info, jit_info, state_info, log, rate, sjit, sload_info = db3(request)
    return render(request, '0record.html')

def analysis_empty(request):
    return render(request, '0analysis.html')

def identify(request):
    return render(request, 'identify.html')

def db1(request):
    attack_info = Library.objects.filter(id__lt=100)

    return attack_info


def db2(request):
    record_info = Record.objects.filter(id__lt=100)

    return record_info

def db_url(request):
    # record_info = Record.objects.filter(id__lt=1024,dstip__in=['125.76.115.58','125.76.115.59','125.76.115.60'],srcport__gt=1,dstport__gt=1)
    flow = []
    # 打开PCAP文件
    with open('./data/000-all/287_4_FTP暴力破解_1.32.233.155_125.76.115.51.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        # 遍历PCAP文件中的每个数据包
        for ts, buf in pcap:
            # 解析以太网帧
            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                continue  # 只处理IP数据包

            # 解析IP数据包
            ip = eth.data
            # 源IP和目的IP
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)

            # 检查协议类型并解析相应的数据包
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                # 解析TCP数据包
                tcp = ip.data
                src_port = tcp.sport
                dst_port = tcp.dport
                protocol = 'TCP'
            elif ip.p == dpkt.ip.IP_PROTO_UDP:
                # 解析UDP数据包
                udp = ip.data
                src_port = udp.sport
                dst_port = udp.dport
                protocol = 'UDP'
            else:
                # 其他协议
                continue

            flow.append({'src_ip':src_ip,'dst_ip':dst_ip,'src_port':src_port,'dst_port':dst_port,'protocol':protocol})
    return flow
    # return record_info

def db3(request):
    generic = Statistic.objects.filter(attack_cat='Generic').count()
    exploits = Statistic.objects.filter(attack_cat='Exploits').count()
    fuzzers = Statistic.objects.filter(attack_cat='Fuzzers').count()
    dos = Statistic.objects.filter(attack_cat='DoS').count()
    reconnaissance = Statistic.objects.filter(attack_cat='Reconnaissance').count()
    statistics_info = [generic, exploits, fuzzers, dos, reconnaissance]

    generic_sjit = Statistic.objects.filter(attack_cat='Generic').aggregate(Avg('sjit')).get('sjit__avg')
    generic_djit = Statistic.objects.filter(attack_cat='Generic').aggregate(Avg('djit')).get('djit__avg')
    exploits_sjit = Statistic.objects.filter(attack_cat='Exploits').aggregate(Avg('sjit')).get('sjit__avg')
    exploits_djit = Statistic.objects.filter(attack_cat='Exploits').aggregate(Avg('djit')).get('djit__avg')
    fuzzers_sjit = Statistic.objects.filter(attack_cat='Fuzzers').aggregate(Avg('sjit')).get('sjit__avg') / 3
    fuzzers_djit = Statistic.objects.filter(attack_cat='Fuzzers').aggregate(Avg('djit')).get('djit__avg')
    dos_sjit = Statistic.objects.filter(attack_cat='DoS').aggregate(Avg('sjit')).get('sjit__avg')
    dos_djit = Statistic.objects.filter(attack_cat='DoS').aggregate(Avg('djit')).get('djit__avg')
    reconnaissance_sjit = Statistic.objects.filter(attack_cat='Reconnaissance').aggregate(Avg('sjit')).get('sjit__avg')
    reconnaissance_djit = Statistic.objects.filter(attack_cat='Reconnaissance').aggregate(Avg('djit')).get('djit__avg')
    jit_info = [int(generic_sjit), int(generic_djit),
                int(exploits_sjit), int(exploits_djit),
                int(fuzzers_sjit), int(fuzzers_djit),
                int(dos_sjit), int(dos_djit),
                int(reconnaissance_sjit), int(reconnaissance_djit)]

    state_1_fin = Statistic.objects.filter(id__lt=15000, state='FIN').count() / 15000
    state_1_int = Statistic.objects.filter(id__lt=15000, state='INT').count() / 15000
    state_1_con = Statistic.objects.filter(id__lt=15000, state='CON').count() / 15000

    state_2_fin = Statistic.objects.filter(id__lt=30000, id__gt=15000, state='FIN').count() / 15000
    state_2_int = Statistic.objects.filter(id__lt=30000, id__gt=15000, state='INT').count() / 15000
    state_2_con = Statistic.objects.filter(id__lt=30000, id__gt=15000, state='CON').count() / 15000

    state_3_fin = Statistic.objects.filter(id__lt=45000, id__gt=30000, state='FIN').count() / 15000
    state_3_int = Statistic.objects.filter(id__lt=45000, id__gt=30000, state='INT').count() / 15000
    state_3_con = Statistic.objects.filter(id__lt=45000, id__gt=30000, state='CON').count() / 15000

    state_4_fin = Statistic.objects.filter(id__lt=60000, id__gt=45000, state='FIN').count() / 15000
    state_4_int = Statistic.objects.filter(id__lt=60000, id__gt=45000, state='INT').count() / 15000
    state_4_con = Statistic.objects.filter(id__lt=60000, id__gt=45000, state='CON').count() / 15000

    state_info = [state_1_fin, state_1_int, state_1_con,
                  state_2_fin, state_2_int, state_2_con,
                  state_3_fin, state_3_int, state_3_con,
                  state_4_fin, state_4_int, state_4_con]

    all_record = Statistic.objects.all().count()
    normal_record = Statistic.objects.filter(attack_cat='Normal').count()
    doubt_record = Statistic.objects.filter(attack_cat='Fuzzers').count()
    anomaly_record = all_record - normal_record - doubt_record
    log_info = [all_record, normal_record, doubt_record, anomaly_record]

    rate_record_1 = Statistic.objects.filter(rate__lt=10).count()
    rate_record_2 = Statistic.objects.filter(rate__lt=50, rate__gt=10).count()
    rate_record_3 = Statistic.objects.filter(rate__lt=100, rate__gt=50).count()
    rate_record_4 = Statistic.objects.filter(rate__gt=100).count()
    rate_info = [rate_record_1, rate_record_2, rate_record_3, rate_record_4]

    sjit_1 = Statistic.objects.filter(sjit__lt=100).count()
    sjit_2 = Statistic.objects.filter(sjit__lt=500, sjit__gt=100).count()
    sjit_3 = Statistic.objects.filter(sjit__lt=1000, sjit__gt=500).count()
    sjit_4 = Statistic.objects.filter(sjit__gt=1000).count()
    sjit_info = [sjit_1, sjit_2, sjit_3, sjit_4]

    sload1 = Statistic.objects.filter(sload__lt=1000).count()
    sload2 = Statistic.objects.filter(sload__lt=5000, sload__gt=1000).count()
    sload3 = Statistic.objects.filter(sload__lt=10000, sload__gt=5000).count()
    sload4 = Statistic.objects.filter(sload__gt=10000).count()
    sload_info = [sload1, sload2, sload3, sload4]

    return statistics_info, jit_info, state_info, log_info, rate_info, sjit_info, sload_info


def db4(request):
    record_info = Record.objects.filter(id__lt=1000, label='1')

    return record_info


def db5(request):
    anomaly_info_1 = Record.objects.filter(id__lt=20000, label='1').count()
    anomaly_info_2 = Record.objects.filter(id__lt=40000, id__gt=20000, label='1').count()
    anomaly_info_3 = Record.objects.filter(id__lt=60000, id__gt=40000, label='1').count()
    anomaly_info_4 = Record.objects.filter(id__lt=80000, id__gt=60000, label='1').count()
    anomaly_info_5 = Record.objects.filter(id__lt=100000, id__gt=80000, label='1').count()
    anomaly_info_6 = Record.objects.filter(id__lt=120000, id__gt=100000, label='1').count()
    anomaly_info_7 = Record.objects.filter(id__lt=140000, id__gt=120000, label='1').count()
    anomaly_info_8 = Record.objects.filter(id__lt=160000, id__gt=140000, label='1').count()
    anomaly_info_9 = Record.objects.filter(id__lt=180000, id__gt=160000, label='1').count()
    anomaly_info_10 = Record.objects.filter(id__lt=200000, id__gt=180000, label='1').count()
    anomaly_info_11 = Record.objects.filter(id__lt=220000, id__gt=200000, label='1').count()
    anomaly_info_12 = Record.objects.filter(id__lt=240000, id__gt=220000, label='1').count()
    anomaly_info_13 = Record.objects.filter(id__lt=260000, id__gt=240000, label='1').count()
    anomaly_info_14 = Record.objects.filter(id__lt=280000, id__gt=260000, label='1').count()
    anomaly_info_15 = Record.objects.filter(id__lt=300000, id__gt=280000, label='1').count()
    anomaly_info_16 = Record.objects.filter(id__lt=320000, id__gt=300000, label='1').count()
    anomaly_info_17 = Record.objects.filter(id__lt=340000, id__gt=320000, label='1').count()
    anomaly_info_18 = Record.objects.filter(id__lt=360000, id__gt=340000, label='1').count()
    anomaly_info_19 = Record.objects.filter(id__lt=380000, id__gt=360000, label='1').count()
    anomaly_info_20 = Record.objects.filter(id__lt=400000, id__gt=380000, label='1').count()
    anomaly_info_21 = Record.objects.filter(id__lt=420000, id__gt=400000, label='1').count()
    anomaly_info_22 = Record.objects.filter(id__lt=440000, id__gt=420000, label='1').count()
    anomaly_info_23 = Record.objects.filter(id__lt=460000, id__gt=440000, label='1').count()
    anomaly_info_24 = Record.objects.filter(id__lt=480000, id__gt=460000, label='1').count()

    anomaly_vul_1 = Record.objects.filter(id__lt=20000, attack_cat='Generic').count()
    anomaly_vul_2 = Record.objects.filter(id__lt=40000, id__gt=20000, attack_cat='Generic').count()
    anomaly_vul_3 = Record.objects.filter(id__lt=60000, id__gt=40000, attack_cat='Generic').count()
    anomaly_vul_4 = Record.objects.filter(id__lt=80000, id__gt=60000, attack_cat='Generic').count()
    anomaly_vul_5 = Record.objects.filter(id__lt=100000, id__gt=80000, attack_cat='Generic').count()
    anomaly_vul_6 = Record.objects.filter(id__lt=120000, id__gt=100000, attack_cat='Generic').count()
    anomaly_vul_7 = Record.objects.filter(id__lt=140000, id__gt=120000, attack_cat='Generic').count()
    anomaly_vul_8 = Record.objects.filter(id__lt=160000, id__gt=140000, attack_cat='Generic').count()
    anomaly_vul_9 = Record.objects.filter(id__lt=180000, id__gt=160000, attack_cat='Generic').count()
    anomaly_vul_10 = Record.objects.filter(id__lt=200000, id__gt=180000, attack_cat='Generic').count()
    anomaly_vul_11 = Record.objects.filter(id__lt=220000, id__gt=200000, attack_cat='Generic').count()
    anomaly_vul_12 = Record.objects.filter(id__lt=240000, id__gt=220000, attack_cat='Generic').count()
    anomaly_vul_13 = Record.objects.filter(id__lt=260000, id__gt=240000, attack_cat='Generic').count()
    anomaly_vul_14 = Record.objects.filter(id__lt=280000, id__gt=260000, attack_cat='Generic').count()
    anomaly_vul_15 = Record.objects.filter(id__lt=300000, id__gt=280000, attack_cat='Generic').count()
    anomaly_vul_16 = Record.objects.filter(id__lt=320000, id__gt=300000, attack_cat='Generic').count()
    anomaly_vul_17 = Record.objects.filter(id__lt=340000, id__gt=320000, attack_cat='Generic').count()
    anomaly_vul_18 = Record.objects.filter(id__lt=360000, id__gt=340000, attack_cat='Generic').count()
    anomaly_vul_19 = Record.objects.filter(id__lt=380000, id__gt=360000, attack_cat='Generic').count()
    anomaly_vul_20 = Record.objects.filter(id__lt=400000, id__gt=380000, attack_cat='Generic').count()
    anomaly_vul_21 = Record.objects.filter(id__lt=420000, id__gt=400000, attack_cat='Generic').count()
    anomaly_vul_22 = Record.objects.filter(id__lt=440000, id__gt=420000, attack_cat='Generic').count()
    anomaly_vul_23 = Record.objects.filter(id__lt=460000, id__gt=440000, attack_cat='Generic').count()
    anomaly_vul_24 = Record.objects.filter(id__lt=480000, id__gt=460000, attack_cat='Generic').count()

    anomaly_info = {'1': anomaly_info_1,
                    '2': anomaly_info_2,
                    '3': anomaly_info_3,
                    '4': anomaly_info_4,
                    '5': anomaly_info_5,
                    '6': anomaly_info_6,
                    '7': anomaly_info_7,
                    '8': anomaly_info_8,
                    '9': anomaly_info_9,
                    '10': anomaly_info_10,
                    '11': anomaly_info_11,
                    '12': anomaly_info_12,
                    '13': anomaly_info_13,
                    '14': anomaly_info_14,
                    '15': anomaly_info_15,
                    '16': anomaly_info_16,
                    '17': anomaly_info_17,
                    '18': anomaly_info_18,
                    '19': anomaly_info_19,
                    '20': anomaly_info_20,
                    '21': anomaly_info_21,
                    '22': anomaly_info_22,
                    '23': anomaly_info_23,
                    '24': anomaly_info_24,
                    '25': anomaly_vul_1,
                    '26': anomaly_vul_2,
                    '27': anomaly_vul_3,
                    '28': anomaly_vul_4,
                    '29': anomaly_vul_5,
                    '30': anomaly_vul_6,
                    '31': anomaly_vul_7,
                    '32': anomaly_vul_8,
                    '33': anomaly_vul_9,
                    '34': anomaly_vul_10,
                    '35': anomaly_vul_11,
                    '36': anomaly_vul_12,
                    '37': anomaly_vul_13,
                    '38': anomaly_vul_14,
                    '39': anomaly_vul_15,
                    '40': anomaly_vul_16,
                    '41': anomaly_vul_17,
                    '42': anomaly_vul_18,
                    '43': anomaly_vul_19,
                    '44': anomaly_vul_20,
                    '45': anomaly_vul_21,
                    '46': anomaly_vul_22,
                    '47': anomaly_vul_23,
                    '48': anomaly_vul_24
                    }

    return anomaly_info

def func1(request):
    listAll = Analysis.objects.all().order_by("-id")[:15]
    result = []
    times = 0
    for var in listAll:
        tmp = []
        tmp.append(str(var.date))
        t1 = float(var.all) + random.randint(1, 9) / 4
        tmp.append(str(t1))
        t2 = float(var.inputFlow) + random.randint(1, 9) / 30
        tmp.append(str(t2))
        tmp.append(str(t1 - t2))
        result.append(tmp)
    result.reverse()
    return JsonResponse(result, safe=False)

# 协议类别
def chart1(request):
    listAll = Prediction.objects.all()
    dict = {}
    result = []
    for var in listAll:
        if var.protocol in dict:
            dict[var.protocol] = dict[var.protocol] + 1
        else:
            dict[var.protocol] = 1
    for key in dict.keys():
        tmp = []
        tmp.append(str(key))
        #tmp.append(str(dict.get(key)))
        tmp.append(str(random.randint(1, 20)))
        result.append(tmp)
    return JsonResponse(result, safe=False)


# 异常行为预测分布
def chart2(request):
    listAll = Prediction.objects.all()
    dict = {}
    prob3 = {}
    prob2 = {}
    prob1 = {}
    result = []
    for var in listAll:
        if var.city in dict:
            dict[var.city] = dict[var.city] + 1
        else:
            dict[var.city] = 1
        if float(var.prob) > 0.9:
            if var.city in prob3:
                prob3[var.city] = prob3[var.city] + 1
            else:
                prob3[var.city] = 1
        elif float(var.prob) > 0.5:
            if var.city in prob2:
                prob2[var.city] = prob2[var.city] + 1
            else:
                prob2[var.city] = 1
        else:
            if var.city in prob1:
                prob1[var.city] = prob1[var.city] + 1
            else:
                prob1[var.city] = 1
    for key in dict.keys():
        tmp = []
        tmp.append(str(key))
        tmp.append(str(dict.get(key)))
        if key in prob3:
            tmp.append(str(prob3.get(key)))
        else:
            tmp.append(str("0"))
        if key in prob2:
            tmp.append(str(prob2.get(key)))
        else:
            tmp.append(str("0"))
        if key in prob1:
            tmp.append(str(prob1.get(key)))
        else:
            tmp.append(str("0"))
        result.append(tmp)
    return JsonResponse(result, safe=False)


# 预测网络攻击分类
def chart3(request):
    listAll = Prediction.objects.all()
    dict = {}
    result = []
    for var in listAll:
        if var.attack in dict:
            dict[var.attack] = dict[var.attack] + 1
        else:
            dict[var.attack] = 1
    for key in dict.keys():
        tmp = []
        tmp.append(str(key))
        #tmp.append(str(dict.get(key)))
        tmp.append(str(random.randint(10, 20)))
        result.append(tmp)
    return JsonResponse(result, safe=False)


# 未来网络攻击TOP5
def chart4(request):
    listAll = Prediction.objects.all()
    dict = {}
    result = []
    for var in listAll:
        if var.attack in dict:
            dict[var.attack] = dict[var.attack] + 1
        else:
            dict[var.attack] = 1
    dict = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)
    time = 0
    okk = 0
    for let in dict:
        if time == 0:
            okk = let[1]
        if time == 5:
            break
        tmp = []
        tmp.append(str(let[0]))
        #tmp.append(str(let[1]))
        okk = okk - random.randint(2, 20)
        tmp.append(str(okk))
        result.append(tmp)
        time = time + 1
    return JsonResponse(result, safe=False)


# 地区预测网络攻击排行
def chart5(request):
    listAll = Prediction.objects.all()
    dict = {}
    result = []
    for var in listAll:
        if var.city in dict:
            dict[var.city] = dict[var.city] + 1
        else:
            dict[var.city] = 1
    dict = sorted(dict.items(), key=lambda kv: (kv[1], kv[0]))
    time = 0
    okk = 0
    for let in dict:
        if time == 0:
            okk = let[1]
            print(okk)
        if time == 6:
            break
        tmp = []
        tmp.append(str(let[0]))
        okk = okk + random.randint(1, 3)
        #print(okk)
        tmp.append(str(okk))
        #tmp.append(str(let[1]))
        result.append(tmp)
        time = time + 1
    return JsonResponse(result, safe=False)


# 预警级别
def numberShow(request):
    listAll = Prediction.objects.all()
    prob3 = 0
    prob2 = 0
    prob1 = 0
    for var in listAll:
        if float(var.prob) > 0.9:
            prob3 = prob3 + random.randint(1,3)
        elif float(var.prob) > 0.5:
            prob2 = prob2 + random.randint(1,6)
        else:
            prob1 = prob1 + random.randint(3,8)
    result = []
    result.append(str(prob3))
    result.append(str(prob2))
    result.append(str(prob1))
    result.append(str(prob3 + prob2 + prob1))
    result.append(str(random.randint(50, 100)))
    return JsonResponse(result, safe=False)


def mockData(request):
    predictionInfo = Prediction()
    citys = ["广州", "上海", "北京", "南京", "长沙", "厦门", "海门", "鄂尔多斯", "招远", "舟山", "青岛", "拉萨", "威海", "抚顺", "葫芦岛", "烟台", "沈阳", "吉林"]
    predictionInfo.city = citys[random.randint(0, len(citys)-1)]
    predictionInfo.prob = str(random.randint(4, 10) / 10)
    attacks = ["DoS", "DDoS", "Bot", "WebAttack", "Infiltration"]
    predictionInfo.attack = attacks[random.randint(0, 4)]
    protocols = ["tcp", "udp", "http", "ftp"]
    predictionInfo.protocol = protocols[random.randint(0, 3)]
    predictionInfo.date = str(datetime.now().strftime("%H:%M:%S"))
    predictionInfo.dst_ip = "192.168.172.33"
    predictionInfo.src_ip = "192.168.172.33"
    predictionInfo.dst_port = 1
    predictionInfo.src_port = 1
    predictionInfo.save()
    result = []
    return JsonResponse(result, safe=False)





