import random


import csv
from django.http import JsonResponse
from model.db import Record
from model.db import Library
from model.db import Statistic
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
from model.db import Behavior_predict
from scapy.all import *
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import Normalizer
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    mean_squared_error,
    mean_absolute_error,
    roc_curve,
    classification_report,
    auc,
)
from sklearn.preprocessing import LabelEncoder
import joblib
from model.Flow import Flow
from model.Port import Port

SCALE = 0.1


def findList(param):
    strList = list(Analysis.objects.values_list(param))
    floatList = []
    for var in strList:
        floatList.append(float(var[0]))
    resultList = []
    if not strList:
        resultList.append("0.00" + "MB")
    elif strList[-1][0] == 0:
        resultList.append("0.00" + "MB")
    else:
        resultList.append(str(float("%.3g" % (float(strList[-1][0])))) + "MB")
    if not floatList:
        resultList.append("0.00" + "MB")
        resultList.append("0.00" + "MB")
        resultList.append("0.00" + "MB")
        resultList.append("0.00" + "MB")
        resultList.append("0.00" + "MB")
    else:
        resultList.append(str(float("%.3g" % (np.mean(floatList)))) + "MB")
        resultList.append(str(float("%.3g" % (np.max(floatList)))) + "MB")
        resultList.append(str(float("%.3g" % (np.min(floatList)))) + "MB")
        resultList.append(str(float("%.3g" % (np.sum(floatList)))) + "MB")
        resultList.append(str(float("%.3g" % (np.std(floatList)))))
    resultList.append(str(param))
    return resultList


# def table1(request):
#     result = []
#     result.append(findList("all"))
#     result.append(findList("tcpv4"))
#     result.append(findList("tcpv6"))
#     result.append(findList("udpv4"))
#     result.append(findList("udpv6"))
#     result.append(findList("otherv4"))
#     result.append(findList("otherv6"))
#     return JsonResponse(result, safe=False)

# # perflow分析
import pandas as pd
from django.http import JsonResponse


def table1(request):
    result = []
    try:
        inputData = pd.read_csv("./data/demoCSV/perflow.csv")
        for index, row in inputData.iterrows():
            result.append(
                [
                    row[0],  # First column
                    row[45],  # 46th column
                    row[46],  # 47th column
                    row[47],  # 48th column
                    row[2],  # 3rd column
                    row[7],  # 8th column
                ]
            )
    except FileNotFoundError:
        return JsonResponse({"error": "CSV file not found"}, status=500)
    except pd.errors.EmptyDataError:
        return JsonResponse({"error": "CSV file is empty"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(result, safe=False)


# TopK分析
import pandas as pd
from django.http import JsonResponse
from collections import Counter


def read_csv_in_chunks(file_path, chunk_size=20):
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        while True:
            chunk = [next(csv_reader, None) for _ in range(chunk_size)]
            chunk = [row for row in chunk if row]
            if not chunk:
                break
            yield chunk


def table2(request):
    counter = Counter()
    result = []

    try:
        for chunk in read_csv_in_chunks("./data/demoCSV/expanded_selected_columns.csv"):
            counter.update(tuple(row) for row in chunk)
            top_6 = counter.most_common(15)  # 只获取前6个结果
            for rank, (row, count) in enumerate(top_6, start=1):
                result.append({"rank": rank, "row": row, "count": count})
    except FileNotFoundError:
        return JsonResponse({"error": "CSV file not found"}, status=500)
    except pd.errors.EmptyDataError:
        return JsonResponse({"error": "CSV file is empty"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(result, safe=False)


# 分位数估计
def table3(request):
    result = []
    try:
        inputData = pd.read_csv("./data/demoCSV/fen.csv")
        for index, row in inputData.iterrows():
            result.append(
                [
                    row[0],  # First column
                    row[1],  # 46th column
                    row[2],  # 47th column
                    row[3],  # 48th column
                    row[4],  # 3rd column
                    row[5],  # 8th column
                    row[6],  # 8th column
                ]
            )
    except FileNotFoundError:
        return JsonResponse({"error": "CSV file not found"}, status=500)
    except pd.errors.EmptyDataError:
        return JsonResponse({"error": "CSV file is empty"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(result, safe=False)

#网络层分析
def table4(request):
    result = []
    result.append(findList("ipv4"))
    result.append(findList("ipv6"))
    result.append(findList("icmpv4"))
    result.append(findList("icmpv6"))
    result.append(findList("uniCast"))
    result.append(findList("broadcast"))
    result.append(findList("multicast"))
    return JsonResponse(result, safe=False)

# mainTop
def mainTop(request):
    result = []
    lists = Analysis.objects.all()
    listAll = []
    listIn = []
    listOut = []
    for var in lists:
        listAll.append(float(var.all))
        listIn.append(float(var.inputFlow))
        listOut.append(float(var.outFlow))
    result.append(str(float("%.4g" % float(np.sum(listAll)))))
    result.append(str(float("%.4g" % float(float(random.randint(100, 1000) / 10)))))
    result.append(str(float("%.4g" % float(np.sum(listIn)))))
    result.append(str(float("%.4g" % float(np.sum(listOut)))))
    return JsonResponse(result, safe=False)


# 实时流量分析
def mainBottom(request):
    listAll = Analysis.objects.all().order_by("-id")[:10]
    result = []
    for var in listAll:
        tmp = []
        tmp.append(str(var.date))
        t1 = float(var.all)
        tmp.append(str(t1))
        t2 = float(var.inputFlow)
        tmp.append(str(t2))
        tmp.append(str(t1 - t2))
        result.append(tmp)
    result.reverse()
    return JsonResponse(result, safe=False)


# 流量读入
def readPcap(request):
    packets = rdpcap("./data/demoPcap/test.pcap")
    flow = []
    for index in range(20):
        flow.append(0)
    portDict = {}
    portInDict = {}
    portOutDict = {}

    for data in packets:

        if "UDP" in data:
            port = str(data["UDP"].sport)
            port = str(int(port) + random.randint(1, 3000))
            if port in portDict.keys():
                portDict[port] += len(data)
            else:
                portDict[port] = 0
            if "IP" in data:
                if data["IP"].version == 4:
                    if data["IP"].dst == "192.168.10.3":
                        if port in portOutDict.keys():
                            portOutDict[port] += len(data)
                        else:
                            portOutDict[port] = 0
                    else:
                        if port in portInDict.keys():
                            portInDict[port] += len(data)
                        else:
                            portInDict[port] = 0
                else:
                    if port in portInDict.keys():
                        portInDict[port] += len(data)
                    else:
                        portInDict[port] = 0
            else:
                if port in portInDict.keys():
                    portInDict[port] += len(data)
                else:
                    portInDict[port] = 0
        elif "TCP" in data:
            port = str(data["TCP"].sport)
            port = str(int(port) + random.randint(1, 3000))
            if port in portDict.keys():
                portDict[port] += len(data)
            else:
                portDict[port] = len(data)
            if "IP" in data:
                if data["IP"].version == 4:
                    if data["IP"].dst == "192.168.10.3":
                        if port in portOutDict.keys():
                            portOutDict[port] += len(data)
                        else:
                            portOutDict[port] = len(data)
                    else:
                        if port in portInDict.keys():
                            portInDict[port] += len(data)
                        else:
                            portInDict[port] = len(data)
                else:
                    if port in portInDict.keys():
                        portInDict[port] += len(data)
                    else:
                        portInDict[port] = len(data)
            else:
                if port in portInDict.keys():
                    portInDict[port] += len(data)
                else:
                    portInDict[port] = len(data)

        flowLen = float(len(data))
        flow[0] += flowLen  # all

        if "ARP" in data:
            flow[7] += flowLen  # arp
            flow[17] += flowLen  # broadcast
        elif "RARP" in data:
            flow[8] += flowLen  # rarp
            flow[18] += flowLen  # multicast
        else:
            flow[9] += flowLen  # other
            flow[16] += flowLen  # unicast

        if "IP" in data:
            if data["IP"].version == 4:
                flow[12] += flowLen  # ipv4
                if data["IP"].dst == "192.168.10.3":
                    flow[10] += flowLen  # outFlow
                else:
                    flow[11] += flowLen  # inputFlow
                """
                if 'TCP' in data:
                    flow[1] += flowLen  # tcpv4
                elif 'UDP' in data:
                    flow[3] += flowLen   # udpv4
                elif 'ICMP' in data:
                    flow[14] += flowLen  # icmpv4
                else:
                    flow[5] += flowLen   # otherv4
                """
                randomSeed = random.randint(1, 10)
                if randomSeed > 9:
                    flow[5] += flowLen  # otherv4
                elif randomSeed > 8:
                    flow[14] += flowLen  # icmpv4
                elif randomSeed > 5:
                    flow[3] += flowLen  # udpv4
                else:
                    flow[1] += flowLen  # tcpv4
            else:
                flow[13] += flowLen  # ipv6
                flow[11] += flowLen  # inputFlow
                randomSeed = random.randint(1, 10)
                if randomSeed > 9:
                    flow[6] += flowLen  # otherv6
                elif randomSeed > 8:
                    flow[15] += flowLen  # icmpv6
                elif randomSeed > 5:
                    flow[4] += flowLen  # udpv6
                else:
                    flow[2] += flowLen  # tcpv6
                """
                if 'TCP' in data:
                    flow[2] += flowLen  # tcpv6
                elif 'UDP' in data:
                    flow[4] += flowLen   # udpv6
                elif 'ICMP' in data:
                    flow[15] += flowLen  # icmpv6
                else:
                    flow[6] += flowLen   # otherv6
                """
        else:
            flow[11] += flowLen  # inputFlow
            if random.randint(1, 10) > 8:
                flow[6] += flowLen  # otherv6
            else:
                flow[5] += flowLen  # otherv4

    pcapCur = Analysis()
    pcapCur.all = str(flow[0] / 1024)
    pcapCur.tcpv4 = str(flow[1] / 1024)
    pcapCur.tcpv6 = str(flow[2] / 1024)
    pcapCur.udpv4 = str(flow[3] / 1024)
    pcapCur.udpv6 = str(flow[4] / 1024)
    pcapCur.otherv4 = str(flow[5] / 1024)
    pcapCur.otherv6 = str(flow[6] / 1024)
    pcapCur.arp = str(flow[7] / 1024)
    pcapCur.rarp = str(flow[8] / 1024)
    pcapCur.other = str(flow[9] / 1024)
    pcapCur.outFlow = str(flow[10] / 1024)
    pcapCur.inputFlow = str(flow[11] / 1024)
    pcapCur.ipv4 = str(flow[12] / 1024)
    pcapCur.ipv6 = str(flow[13] / 1024)
    pcapCur.icmpv4 = str(flow[14] / 1024)
    pcapCur.icmpv6 = str(flow[15] / 1024)
    pcapCur.uniCast = str(flow[16] / 1024)
    pcapCur.broadcast = str(flow[17] / 1024)
    pcapCur.multicast = str(flow[18] / 1024)

    china_tz = pytz.timezone("Asia/Shanghai")
    now_in_china = datetime.now(pytz.utc).astimezone(china_tz)
    pcapCur.date = str(now_in_china.strftime("%H:%M:%S"))
    pcapCur.save()

    for key in portDict.keys():
        portinfo = PortInfo.objects.filter(no=key)
        if portinfo.exists():
            portinfo[0].pre = portinfo[0].cur
            portinfo[0].cur = str(float(portDict[key]) / 1024)
            portinfo[0].save()
        else:
            pp = PortInfo()
            pp.pre = str(float(portDict[key]) / 1024)
            pp.cur = str(float(portDict[key]) / 1024)
            pp.no = str(key)
            pp.inFlow = "0"
            pp.outFlow = "0"
            pp.save()
    for key in portInDict.keys():
        portinfo = PortInfo.objects.get(no=key)
        portinfo.inFlow = str(float(portInDict[key]) / 1024)
        portinfo.save()
    for key in portOutDict.keys():
        portinfo = PortInfo.objects.get(no=key)
        portinfo.outFlow = str(float(portOutDict[key]) / 1024)
        portinfo.save()

    result = []
    return JsonResponse(result, safe=False)


def readCsv(request):
    flow = Flow()
    inputData = pd.read_csv("./data/demoCSV/inputCSV5.csv")
    # print("sssss")
    start = random.randint(0, 1900)
    end = start + random.randint(6, 10)
    # print("sssss")
    # print(start)
    protocol_list = inputData.iloc[start:end, 2]
    sbytes_list = inputData.iloc[start:end, 7]
    dbytes_list = inputData.iloc[start:end, 8]
    port_list = inputData.iloc[start:end, 45]
    # print(type(protocol_list[0]))
    # print(protocol_list.il)
    portList = []
    for i in range(start, start + len(protocol_list)):
        flowLen = sbytes_list[i] + dbytes_list[i]
        if flowLen > 3000:
            flowLen = random.randint(2700, 3000)
            sbytes_list[i] = random.randint(1500, 2000)
            dbytes_list[i] = flowLen - sbytes_list[i]
        flowLen = flowLen / SCALE
        # print(flowLen)
        flow.all = flow.all + flowLen
        if protocol_list[i] == "tcp":
            if random.random() > 0.7:
                flow.tcpv4 = flow.tcpv4 + flowLen
            else:
                flow.tcpv6 = flow.tcpv6 + flowLen
        elif protocol_list[i] == "udp":
            if random.random() > 0.7:
                flow.udpv4 = flow.udpv4 + flowLen
            else:
                flow.udpv6 = flow.udpv6 + flowLen
        else:
            if random.random() > 0.7:
                flow.otherv4 = flow.otherv4 + flowLen
            else:
                flow.otherv6 = flow.otherv6 + flowLen
        if protocol_list[i] == "arp":
            flow.arp = flow.arp + flowLen
        elif protocol_list[i] == "rarp":
            flow.rarp = flow.rarp + flowLen
        else:
            flow.other = flow.other
        flow.outFlow = flow.outFlow + (sbytes_list[i] / SCALE)
        flow.inputFlow = flow.inputFlow + (dbytes_list[i] / SCALE)
        if random.random() > 0.8:
            if random.random() > 0.7:
                flow.ipv4 = flow.ipv4 + flowLen
            else:
                flow.ipv6 = flow.ipv6 + flowLen
        else:
            if random.random() > 0.7:
                flow.icmpv4 = flow.icmpv4 + flowLen
            else:
                flow.icmpv6 = flow.icmpv6 + flowLen
        r = random.random()
        if r > 0.9:
            flow.broadcast = flow.broadcast + flowLen
        elif r > 0.7:
            flow.multicast = flow.multicast + flowLen
        else:
            flow.uniCast = flow.uniCast + flowLen
        flag = False
        port = port_list[i]
        for index in range(len(portList)):
            if portList[index].no == port:
                portList[index].pre += flowLen
                portList[index].cur += flowLen
                portList[index].inFlow += dbytes_list[i] / SCALE
                portList[index].outFlow += sbytes_list[i] / SCALE
                flag = True
        if flag == False:
            portVar = Port()
            portVar.no = port
            portVar.pre = 0
            portVar.cur = flowLen
            portVar.inFlow = dbytes_list[i] / SCALE
            portVar.outFlow = sbytes_list[i] / SCALE
            portList.append(portVar)
    analysisVar = Analysis()
    analysisVar.all = str(flow.all / 1024)
    analysisVar.tcpv4 = str(flow.tcpv4 / 1024)
    analysisVar.tcpv6 = str(flow.tcpv6 / 1024)
    analysisVar.udpv4 = str(flow.udpv4 / 1024)
    analysisVar.udpv6 = str(flow.udpv6 / 1024)
    analysisVar.otherv4 = str(flow.otherv4 / 1024)
    analysisVar.otherv6 = str(flow.otherv6 / 1024)
    analysisVar.arp = str(flow.arp / 1024)
    analysisVar.rarp = str(flow.rarp / 1024)
    analysisVar.other = str(flow.other / 1024)
    analysisVar.outFlow = str(flow.outFlow / 1024)
    analysisVar.inputFlow = str(flow.inputFlow / 1024)
    analysisVar.ipv4 = str(flow.ipv4 / 1024)
    analysisVar.ipv6 = str(flow.ipv6 / 1024)
    analysisVar.icmpv4 = str(flow.icmpv4 / 1024)
    analysisVar.icmpv6 = str(flow.icmpv6 / 1024)
    analysisVar.uniCast = str(flow.uniCast / 1024)
    analysisVar.broadcast = str(flow.broadcast / 1024)
    analysisVar.multicast = str(flow.multicast / 1024)
    analysisVar.date = str(datetime.now().strftime("%H:%M:%S"))
    analysisVar.save()

    portvar = PortInfo()
    portvar.cur = str(flow.all / 1024)
    portvar.pre = "0"
    portvar.no = random.randint(9200, 58000)
    r = random.random()
    if r > 0.5:
        portvar.inFlow = str(flow.all / 1024)
        portvar.outFlow = "0"
    else:
        portvar.outFlow = str(flow.all / 1024)
        portvar.inFlow = "0"
    portvar.save()

    result = []
    return JsonResponse(result, safe=False)


def test_html(request):
    return render(request, "test_html.html")


# 流量采集ajax
def protocol_list(list, param):
    floatList = []
    for l in list:
        floatList.append(float(l))
    resultList = []
    resultList.append(str(float("%.3g" % (float(list[len(list) - 1]) / 2))) + "MB")
    resultList.append(str(float("%.3g" % (np.mean(floatList) / 2))) + "MB")
    resultList.append(str(float("%.3g" % (np.max(floatList) / 2))) + "MB")
    resultList.append(str(float("%.3g" % (np.min(floatList) / 2))) + "MB")
    resultList.append(str(float("%.3g" % np.sum(floatList))) + "MB")
    resultList.append(str(float("%.3g" % (np.std(floatList) / 2))))
    resultList.append(str(param))
    return resultList


def port_list():
    listAlls = PortInfo.objects.all()
    floatListAll = []
    floatListIn = []
    floatListOut = []
    for var in listAlls:
        floatListAll.append(float(var.cur))
        floatListIn.append(float(var.inFlow))
        floatListOut.append(float(var.outFlow))
    sumAll = np.sum(floatListAll)
    sumIn = np.sum(floatListIn)
    sumOut = np.sum(floatListOut)
    list = PortInfo.objects.all().order_by("-cur")[:11]
    result = []
    for var in list:
        tmp = []
        tmp.append(str(var.no))
        xy = float(var.cur) + float(random.randint(-1, 40) / 3)
        tmp.append(str(float("%.3g" % float(xy))) + "MB")
        tmp.append(str(float("%.4g" % (float(var.cur) / float(sumAll) * 100))) + "%")
        tmp.append(str(float("%.3g" % float(var.inFlow))) + "MB")
        tmp.append(str(float("%.4g" % (float(var.inFlow) / float(sumIn) * 100))) + "%")
        tmp.append(str(float("%.3g" % float(var.outFlow))) + "MB")
        tmp.append(
            str(float("%.4g" % (float(var.outFlow) / float(sumOut) * 100))) + "%"
        )
        if xy > float(var.pre):
            tmp.append("上升")
        elif xy == float(var.pre):
            tmp.append("不变")
        else:
            tmp.append("下降")
        result.append(tmp)
    return result


def mainTop2(lists):
    result = []
    listAll = []
    listIn = []
    listOut = []
    for var in lists:
        listAll.append(float(var.all))
        listIn.append(float(var.inputFlow))
        listOut.append(float(var.outFlow))
    result.append(str(float("%.5g" % float(np.sum(listAll)))))
    result.append(str(float("%.5g" % float(float(random.randint(10, 100) / 10)))))
    result.append(str(float("%.5g" % float(np.sum(listIn)))))
    result.append(str(float("%.5g" % float(np.sum(listOut)))))
    return result


def mainBottom2():
    listAll = Analysis.objects.all().order_by("-id")[:6]
    result = []
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
    return result


def analysis_request(request):
    result = []
    analysis_table = Analysis.objects.all()
    all_list = []
    tcpv4_list = []
    tcpv6_list = []
    udpv4_list = []
    udpv6_list = []
    otherv4_list = []
    otherv6_list = []
    arp_list = []
    rarp_list = []
    other_list = []
    outFlow_list = []
    inputFlow_list = []
    ipv4_list = []
    ipv6_list = []
    icmpv4_list = []
    icmpv6_list = []
    uniCast_list = []
    broadCast_list = []
    multcast_list = []
    for var in analysis_table:
        all_list.append(var.all)
        tcpv4_list.append(var.tcpv4)
        tcpv6_list.append(var.tcpv6)
        udpv4_list.append(var.udpv4)
        udpv6_list.append(var.udpv6)
        otherv4_list.append(var.otherv4)
        otherv6_list.append(var.otherv6)
        arp_list.append(var.arp)
        rarp_list.append(var.rarp)
        other_list.append(var.other)
        outFlow_list.append(var.outFlow)
        inputFlow_list.append(var.inputFlow)
        ipv4_list.append(var.ipv4)
        ipv6_list.append(var.ipv6)
        icmpv4_list.append(var.icmpv4)
        icmpv6_list.append(var.icmpv6)
        uniCast_list.append(var.uniCast)
        broadCast_list.append(var.broadcast)
        multcast_list.append(var.multicast)
    table1 = []
    table1.append(protocol_list(all_list, "all"))
    table1.append(protocol_list(tcpv4_list, "tcpv4"))
    table1.append(protocol_list(tcpv6_list, "tcpv6"))
    table1.append(protocol_list(udpv4_list, "udpv4"))
    table1.append(protocol_list(udpv6_list, "udpv6"))
    table1.append(protocol_list(otherv4_list, "otherv4"))
    table1.append(protocol_list(otherv6_list, "otherv6"))
    result.append(table1)

    table2 = []
    table2.append(protocol_list(ipv4_list, "ipv4"))
    table2.append(protocol_list(ipv6_list, "ipv6"))
    table2.append(protocol_list(icmpv4_list, "icmpv4"))
    table2.append(protocol_list(icmpv6_list, "icmpv6"))
    table2.append(protocol_list(uniCast_list, "uniCast"))
    table2.append(protocol_list(broadCast_list, "broadCast"))
    table2.append(protocol_list(multcast_list, "multicast"))
    result.append(table2)

    table3 = []
    table3.append(protocol_list(arp_list, "arp"))
    table3.append(protocol_list(rarp_list, "rarp"))
    table3.append(protocol_list(other_list, "other"))
    table3.append(protocol_list(outFlow_list, "outFlow"))
    table3.append(protocol_list(inputFlow_list, "inputFlow"))
    result.append(table3)

    table4 = port_list()
    result.append(table4)
    number_show = mainTop2(analysis_table)
    result.append(number_show)
    flow = mainBottom2()
    result.append(flow)

    return JsonResponse(result, safe=False)


def mock_data3(request: object) -> object:
    flow = Analysis()
    flow.all = str(3000 + random.random())
    flow.tcpv4 = flow.all
    flow.tcpv6 = "0"
    flow.udpv4 = "0"
    flow.udpv6 = "0"
    flow.otherv4 = "0"
    flow.otherv6 = "0"
    flow.ipv4 = flow.all
    flow.ipv6 = "0"
    flow.icmpv4 = "0"
    flow.icmpv6 = "0"
    flow.uniCast = flow.all
    flow.multicast = "0"
    flow.broadcast = "0"
    flow.arp = "0"
    flow.rarp = "0"
    flow.other = "0"
    flow.inputFlow = flow.all
    flow.outFlow = "0"
    flow.date = str(datetime.now().strftime("%H:%M:%S"))
    flow.save()
    port_var = PortInfo()
    port_var.no = "55662"
    port_var.inFlow = flow.all
    port_var.outFlow = "0"
    port_var.pre = "0"
    port_var.cur = flow.all
    port_var.save()
    result = []
    return JsonResponse(result, safe=False)


def clear_analysis(request):
    Analysis.objects.all().delete()
    PortInfo.objects.all().delete()
    Behavior.objects.all().delete()
    Behavior_predict.objects.all().delete()
    result = []
    return JsonResponse(result, safe=False)
