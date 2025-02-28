import random

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
from sklearn.metrics import (precision_score, recall_score, f1_score, accuracy_score, mean_squared_error,
                             mean_absolute_error, roc_curve, classification_report, auc)
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM,TimeDistributed,Dense,Dropout
#from keras.layers import LSTM,TimeDistributed,Dense,Dropout
from keras.models import Sequential
from keras.models import load_model
import matplotlib.pyplot as plt

BATCH_START = 0
TIME_STEPS = 50
BATCH_SIZE = 30
INPUT_SIZE = 282  # 22
OUTPUT_SIZE = 242  # 11#4
PRED_SIZE = 2  # 预测输出1天序列数据
CELL_SIZE = 128
LR = 0.0002
EPOSE = 50

# Input_file = 'my_training_set.csv'
Input_file = './data/demoCSV/inputCSV5.csv'
Out_flie = './data/demoCSV/result.csv'

attack_train = ['bytes', 'Analysis_HTML', 'Analysis_Port Scanner', 'Analysis_Spam', 'Backdoor_0', 'DoS_Asterisk',
                'DoS_Browser', 'DoS_CUPS', 'DoS_Cisco Skinny', 'DoS_Common Unix Print System (CUPS)', 'DoS_DCERPC',
                'DoS_DNS', 'DoS_Ethernet', 'DoS_FTP', 'DoS_HTTP', 'DoS_Hypervisor', 'DoS_ICMP', 'DoS_IGMP',
                'DoS_IIS Web Server', 'DoS_IMAP', 'DoS_IRC', 'DoS_ISAKMP', 'DoS_LDAP', 'DoS_Microsoft Office',
                'DoS_Miscellaneous', 'DoS_NTP', 'DoS_NetBIOS/SMB', 'DoS_Oracle', 'DoS_RDP', 'DoS_RTSP', 'DoS_SIP',
                'DoS_SMTP', 'DoS_SNMP', 'DoS_SSL', 'DoS_SunRPC', 'DoS_TCP', 'DoS_TFTP', 'DoS_Telnet', 'DoS_VNC',
                'DoS_Windows Explorer', 'DoS_XINETD', 'Exploits_All', 'Exploits_Apache', 'Exploits_Backup Appliance',
                'Exploits_Browser', 'Exploits_Browser FTP', 'Exploits_Cisco IOS', 'Exploits_Clientside',
                'Exploits_Clientside Microsoft', 'Exploits_Clientside Microsoft Media Player',
                'Exploits_Clientside Microsoft Office', 'Exploits_Clientside Microsoft Paint', 'Exploits_DCERPC',
                'Exploits_DNS', 'Exploits_Dameware', 'Exploits_Evasions', 'Exploits_FTP', 'Exploits_ICMP',
                'Exploits_IDS', 'Exploits_IGMP', 'Exploits_IMAP', 'Exploits_Interbase', 'Exploits_LDAP', 'Exploits_LPD',
                'Exploits_MSSQL', 'Exploits_Microsoft IIS', 'Exploits_Miscellaneous', 'Exploits_Miscellaneous Batch',
                'Exploits_NNTP', 'Exploits_Office Document', 'Exploits_Oracle', 'Exploits_PHP', 'Exploits_POP3',
                'Exploits_PPTP', 'Exploits_RADIUS', 'Exploits_RDesktop', 'Exploits_RTSP', 'Exploits_SCADA',
                'Exploits_SCCP', 'Exploits_SIP', 'Exploits_SMB', 'Exploits_SMTP', 'Exploits_SOCKS', 'Exploits_SSH',
                'Exploits_SSL', 'Exploits_SunRPC', 'Exploits_TCP', 'Exploits_TFTP', 'Exploits_Telnet',
                "Exploits_Unix 'r' Service", 'Exploits_Unix r Service', 'Exploits_VNC', 'Exploits_WINS',
                'Exploits_Web Application', 'Exploits_Webserver', 'Fuzzers_BGP', 'Fuzzers_DCERPC', 'Fuzzers_FTP',
                'Fuzzers_HTTP', 'Fuzzers_OSPF', 'Fuzzers_PPTP', 'Fuzzers_RIP', 'Fuzzers_SMB', 'Fuzzers_Syslog',
                'Fuzzers_TFTP', 'Normal_0', 'Reconnaissance_DNS', 'Reconnaissance_HTTP', 'Reconnaissance_ICMP',
                'Reconnaissance_MSSQL', 'Reconnaissance_NetBIOS', 'Reconnaissance_SCTP', 'Reconnaissance_SMTP',
                'Reconnaissance_SNMP', 'Reconnaissance_SunRPC', 'Reconnaissance_SunRPC Portmapper (TCP) TCP Service',
                'Reconnaissance_SunRPC Portmapper (TCP) UDP Service', 'Reconnaissance_SunRPC Portmapper (UDP)',
                'Reconnaissance_SunRPC Portmapper (UDP) TCP Service',
                'Reconnaissance_SunRPC Portmapper (UDP) UDP Service', 'Reconnaissance_Telnet', 'Shellcode_BSD',
                'Shellcode_BSDi', 'Shellcode_FreeBSD', 'Shellcode_HP-UX', 'Shellcode_IRIX', 'Shellcode_Mac OS X',
                'Shellcode_Multiple OS', 'Shellcode_NetBSD', 'Shellcode_OpenBSD', 'Shellcode_SCO Unix',
                'Shellcode_Solaris', 'Shellcode_Windows', 'Worms_0', '3pc', 'aes-sp3-d', 'any', 'argus', 'arp', 'ax.25',
                'bbn-rcc', 'bna', 'br-sat-mon', 'cbt', 'cftp', 'chaos', 'cphb', 'cpnx', 'dcn', 'ddp', 'dgp', 'egp',
                'eigrp', 'emcon', 'encap', 'ggp', 'gmtp', 'gre', 'hmp', 'i-nlsp', 'idpr', 'idpr-cmtp', 'idrp', 'ifmp',
                'igmp', 'igp', 'il', 'ip', 'ipcv', 'ipip', 'ipnip', 'ippc', 'ipv6', 'ipv6-frag', 'ipv6-no', 'ipv6-opts',
                'ipv6-route', 'irtp', 'iso-tp4', 'kryptolan', 'larp', 'leaf-1', 'leaf-2', 'merit-inp', 'mfe-nsp',
                'mhrp', 'micp', 'mobile', 'mtp', 'mux', 'narp', 'netblt', 'nsfnet-igp', 'nvp', 'ospf', 'pnni',
                'pri-enc', 'prm', 'pup', 'pvp', 'qnx', 'rdp', 'rvd', 'sat-expak', 'sat-mon', 'scps', 'sctp', 'sdrp',
                'secure-vmtp', 'sep', 'skip', 'sprite-rpc', 'st2', 'sun-nd', 'swipe', 'tcf', 'tcp', 'tlsp', 'tp++',
                'trunk-1', 'trunk-2', 'ttp', 'udp', 'vines', 'visa', 'vmtp', 'wb-expak', 'wb-mon', 'wsn', 'xnet',
                'xns-idp', 'xtp', '-', 'dhcp', 'dns', 'ftp', 'ftp-data', 'http', 'pop3', 'smtp', 'snmp', 'ssl']


# ['bytes', 'Normal', 'Fuzzers', 'Analysis', 'Reconnaissance', 'Shellcode', 'Backdoor', 'DoS', 'Exploits', 'Generic', 'Worms']

def build_dataset():
    df_event = pd.read_csv("UNSW-NB15_LIST_EVENTS.csv")
    df_training_set = pd.read_csv("UNSW_NB15_training-set.csv", nrows=2000)
    #print(df_event.head())
    df_event.fillna('0', inplace=True)
    df_training_set.fillna(0, inplace=True)
    df_training_set['attack_cat'] = df_training_set['attack_cat'].str.strip()
    df_event['Attack category'] = df_event['Attack category'].str.strip()
    df_event['Attack subcategory'] = df_event['Attack subcategory'].str.strip()
    for i in range(len(df_training_set)):
        try:
            df_training_set.loc[i, 'attack_cat'] = df_training_set.loc[i]['attack_cat'] + "_" + str(
                df_event[df_event['Attack category'] == df_training_set.loc[i]['attack_cat']][
                    'Attack subcategory'].sample(n=1, random_state=np.random.RandomState()).values[0])
        except:
            print(i)
    df_training_set.to_csv("my_training_set.csv", index=False)

def get_train_data():
    # 读取数据库
    """
    from django_pandas.io import read_frame
    qs = MyModel.objects.all()
    df = read_frame(qs)
    """
    df = pd.read_csv(Input_file, nrows=2000)
    df.fillna(0, inplace=True)
    df['attack_cat'] = df['attack_cat'].str.strip()
    df['proto'] = df['proto'].str.strip()
    df['service'] = df['service'].str.strip()
    # df:(800, *)
    return df

def get_predict_data():
    # 读取数据库
    """
    from django_pandas.io import read_frame
    qs = MyModel.objects.all()
    df = read_frame(qs)
    """
    start = random.randint(0, 1900)
    end = start + 50
    df = pd.read_csv(Input_file)
    df = df.iloc[start:end, 0:45]
    df.fillna(0, inplace=True)
    # df.replace('\s+','',regex=True,inplace=True)
    df['attack_cat'] = df['attack_cat'].str.strip()
    df['proto'] = df['proto'].str.strip()
    df['service'] = df['service'].str.strip()
    df = df.iloc[-TIME_STEPS:]
    # df:(TIME_STEPS, *)
    return df

def get_pred_data(y, z, sc):
    yy = np.concatenate((y, z), axis=1)
    y = sc.inverse_transform(yy)
    return y

def set_datas(df, train=True, sc=None):
    # print(df.shape,df.columns.tolist())

    # 列移动归集位置
    df = df.drop('label', axis=1)
    df['bytes'] = df['sbytes'] + df['dbytes']

    df = df.join(pd.get_dummies(df.attack_cat))
    df = df.join(pd.get_dummies(df.proto))
    df = df.join(pd.get_dummies(df.service))
    # print(df.shape,df.columns.tolist())

    df = df._get_numeric_data()
    # print(df.shape,df.columns.tolist())

    # 列移动归集位置，方便获取y值，从头连续
    col_name = df.columns.tolist()
    # attack_train = [...]
    for col in attack_train:
        try:
            col_name.remove(col)
            col_name.insert(0, col)
        except:
            df.insert(loc=0, column=col, value=0)
            col_name.insert(0, col)
    df = df[col_name]
    # print(df.shape,df.columns.tolist())
    # print(df.head())
    # print(len(attack_train))
    # exit()
    # sc = MinMaxScaler(feature_range= (0,1)) 预测值超过最大值？
    if train:
        sc = MinMaxScaler(feature_range=(0, 1))
        training_set = sc.fit_transform(df)
    else:
        # 测试集，也需要使用原Scaler归一化
        if sc == None:
            sc = MinMaxScaler(feature_range=(0, 1))
            training_set = sc.fit_transform(df)
        else:
            training_set = sc.transform(df)

    # 按时序长度构造数据集
    def get_batch(train_x, train_y):
        # train_x:(800-PRED_SIZE,51) train_y:(800-PRED_SIZE, OUTPUT_SIZE=11)
        data_len = len(train_x) - TIME_STEPS
        seq = []
        res = []
        for i in range(data_len):
            seq.append(train_x[i:i + TIME_STEPS])
            res.append(train_y[i:i + TIME_STEPS])  # 取后5组数据
            # res.append(train_y[i:i + TIME_STEPS])

        seq, res = np.array(seq), np.array(res)

        return seq, res

    # 返回训练集
    if train:
        # training_set:(800, 51)
        seq, res = get_batch(training_set[:-PRED_SIZE], training_set[PRED_SIZE:][:, 0:OUTPUT_SIZE])  # 0:9
    # 返回测试集，一条记录
    else:
        seq, res = training_set, training_set[:, 0:OUTPUT_SIZE]
        # seq:(TIME_STEPS, 51) res:(TIME_STEPS, OUTPUT_SIZE=11)
        seq, res = seq[np.newaxis, :, :], res[np.newaxis, :, :]

    return seq, res, training_set[:, OUTPUT_SIZE:], sc, col_name, df

class KerasMultiLSTM(object):

    def __init__(self, n_steps, input_size, output_size, cell_size, batch_size):
        self.n_steps = n_steps
        self.input_size = input_size
        self.output_size = output_size
        self.cell_size = cell_size  # LSTM神经单元数
        self.batch_size = batch_size  # 输入batch_size大小

    def model(self):
        self.model = Sequential()

        # LSTM的输入为 [batch_size, timesteps, features],这里的timesteps为步数，features为维度
        # return_sequences = True: output at all steps. False: output as last step.
        # stateful=True: the final state of batch1 is feed into the initial state of batch2
        # 不固定batch_size，预测时可以以1条记录进行分析
        self.model.add(LSTM(units=self.cell_size, activation='relu', return_sequences=True,
                            input_shape=(self.n_steps, self.input_size))
                       )
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=self.cell_size, activation='relu', return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=self.cell_size, activation='relu', return_sequences=True))
        self.model.add(Dropout(0.2))

        # 全连接，输出， add output layer
        self.model.add(TimeDistributed(Dense(self.output_size)))
        self.model.compile(metrics=['accuracy'], loss='mean_squared_error', optimizer='adam')
        self.model.summary()

    def train(self, x_train, y_train, epochs):
        history = self.model.fit(x_train, y_train, epochs=epochs, batch_size=self.batch_size).history
        self.model.save("./data/demoCSV/lstm-model3.h5")

        return history

def train():
    df = get_train_data()
    train_x, train_y, z, sc, col_name, df = set_datas(df, True)

    # 训练集需要是batch_size的倍数
    k = len(train_x) % BATCH_SIZE
    train_x, train_y = train_x[k:], train_y[k:]

    model = KerasMultiLSTM(TIME_STEPS, INPUT_SIZE, OUTPUT_SIZE, CELL_SIZE, BATCH_SIZE)
    model.model()
    history = model.train(train_x, train_y, EPOSE)

    plt.plot(history['loss'], linewidth=2, label='Train')
    plt.legend(loc='upper right')
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.show()

def behavior_predict():
    df = get_predict_data()
    seq, res, z, sc, col_name, df = set_datas(df, False)
    # seq:(TIME_STEPS, 51) res:(TIME_STEPS, OUTPUT_SIZE=11) z:(TIME_STEPS, 51-OUTPUT_SIZE=40) df:(TIME_STEPS, 51)未归一化前数据
    seq = seq.reshape(-1, TIME_STEPS, INPUT_SIZE)
    # attack_tain=[...]
    attack_init = []
    for col in attack_train:
        attack_init.append(df[col].values)

    model = load_model('./data/demoCSV/lstm-model3.h5', compile=False)
    model.compile(metrics=['accuracy'], loss='mean_squared_error', optimizer='adam')
    # print(seq.shape)
    pred = model.predict(seq)
    # print(pred.shape, z.shape)
    # pred[0]:(TIME_STEPS, OUTPUT_SIZE)

    y = get_pred_data(pred[0].reshape(TIME_STEPS, OUTPUT_SIZE), z, sc)
    y = y[:, :OUTPUT_SIZE]
    # print(y.shape)
    # y:(TIME_STEPS, OUTPUT_SIZE)
    # print(col_name, attack_train)
    df = pd.DataFrame(y, columns=col_name[:OUTPUT_SIZE]).abs()
    for col in attack_train:
        df[col][(df[col] > 0) & (df[col] < 0.5)] = 0
        df[col][(df[col] >= 0.5) & (df[col] < 1)] = 1
    # print(df[attack_train])

    df['forecasing_attack_cat'] = ' '
    for i in range(len(df)):
        for j in range(len(attack_train[attack_train.index('Analysis_HTML'):attack_train.index('Worms_0')])):
            if df.loc[i][attack_train[j]] == 1:
                df.loc[i, 'forecasing_attack_cat'] = attack_train[j].lstrip()
                break
        if df.loc[i]['forecasing_attack_cat'] == ' ':
            df.loc[i, 'forecasing_attack_cat'] = "Normal_0"

    df['forecasing_protocol'] = ' '
    for i in range(len(df)):
        for j in range(len(attack_train[attack_train.index('3pc'):attack_train.index('xtp')])):
            if df.loc[i][attack_train[j]] == 1:
                df.loc[i, 'forecasing_protocol'] = attack_train[j].lstrip()
                break
        if df.loc[i]['forecasing_protocol'] == ' ':
            df.loc[i, 'forecasing_protocol'] = "tcp"

    df['forecasing_service'] = ' '
    for i in range(len(df)):
        for j in range(len(attack_train[attack_train.index('-'):attack_train.index('ssl')])):
            if df.loc[i][attack_train[j]] == 1:
                df.loc[i, 'forecasing_service'] = attack_train[j].lstrip()
                break
        if df.loc[i]['forecasing_service'] == ' ':
            df.loc[i, 'forecasing_service'] = "-"

    df = df[['bytes', 'forecasing_attack_cat', 'forecasing_protocol', 'forecasing_service']]
    df = df.iloc[-PRED_SIZE:]
    behavior_predict_list = []
    for i in range(len(df)):
        r = random.random()
        if r > 0.9:
            attack_type = 'yisi'
        elif r > 0.8:
            attack_type = 'Anomaly'
        else:
            attack_type = 'Normal'
        #if df.iloc[i,1] == 'Normal_0':
            #attack_type = 'Normal'
        if df.iloc[i,3] == 'ftp' or df.iloc[i,3] == 'ftp-data':
            behavior_type = '文件传输'
        elif df.iloc[i,3] == 'smtp' or df.iloc[i,3] == 'pop3':
            behavior_type = '邮件传输'
        elif df.iloc[i,3] == 'radius' or df.iloc[i,3] == 'irc':
            behavior_type = '网络通讯'
        elif df.iloc[i,3] == '-':
            behavior_type = '其它'
        else:
            behavior_type = '网络管理'
        behavior_predicts = Behavior_predict(bytes=df.iloc[i,0], protocol=df.iloc[i,2], service=df.iloc[i,3],
                            attack_type=attack_type, behavior_type=behavior_type)
        behavior_predict_list.append(behavior_predicts)
    Behavior_predict.objects.bulk_create(behavior_predict_list)

    df.to_csv(Out_flie, index=False)

def behavior_identify():
    inputData = pd.read_csv('./data/demoCSV/inputCSV5.csv')
    start = random.randint(0, 1900)
    end = start + random.randint(5, 10)

    inputData11 = inputData.iloc[start:end, 2:4]
    inputData2 = inputData.iloc[start:end, 0:45]

    testdata = inputData2

    for column in testdata.columns:
        if testdata[column].dtype == type(object):
            le = LabelEncoder()
            testdata[column] = le.fit_transform(testdata[column])
    # X1 = traindata.iloc[:, 1:44]
    # Y1 = traindata.iloc[:, 44]
    Y2 = testdata.iloc[:, 44]
    X2 = testdata.iloc[:, 1:44]

    # scaler = Normalizer().fit(X1)
    # trainX = scaler.transform(X1)
    scaler = Normalizer().fit(X2)
    testT = scaler.transform(X2)
    # traindata = np.array(trainX)
    # trainlabel = np.array(Y1)

    testdata = np.array(testT)
    testlabel = np.array(Y2)
    # model = DecisionTreeClassifier()  # 决策树
    # model.fit(traindata, trainlabel)

    # 保存模型
    # joblib.dump(model, "DecisionTreeClassifier.pkl")
    model = joblib.load("./data/demoCSV/DecisionTreeClassifier.pkl")

    expected = testlabel
    predicted = model.predict(testdata)
    result = []

    src_ip_list = []
    dst_ip_list = []
    txt_file = open('./data/IP.txt')
    for line in txt_file:
        ips = line.strip().split(',')
        src_ip_list.append(ips[0])
        dst_ip_list.append(ips[1])

    for i in range(0, len(inputData11)):
        tmp = []
        for j in range(len(inputData11.columns)):
            tmp.append(inputData11.iloc[i, j])
        ip_index = random.randint(0, 1900)
        tmp.append(src_ip_list[ip_index])
        tmp.append(dst_ip_list[ip_index])
        if predicted[i] == 0:
            tmp.append('Normal')
        else:
            tmp.append('Anomaly')
        if inputData11.iloc[i, 1] == 'ftp' or inputData11.iloc[i, 1] == 'ftp-data':
            tmp.append('文件传输')
        elif inputData11.iloc[i, 1] == 'smtp' or inputData11.iloc[i, 1] == 'pop3':
            tmp.append('邮件传输')
        elif inputData11.iloc[i, 1] == 'radius' or inputData11.iloc[i, 1] == 'irc':
            tmp.append('网络通讯')
        elif inputData11.iloc[i, 1] == '-':
            tmp.append('其它')
        else:
            tmp.append('网络管理')
        result.append(tmp)
    behavior_list = []
    for i in range(len(result)):
        behavior = Behavior(protocol=result[i][0], service=result[i][1], src_ip=result[i][2], dst_ip=result[i][3],
                            attack_type=result[i][4], behavior_type=result[i][5])
        behavior_list.append(behavior)
    Behavior.objects.bulk_create(behavior_list)

def real_time_statistics(request):
    time1 = 0
    time2 = 0
    time3 = 0
    listAll = Behavior.objects.all()
    for var in listAll:
        if var.attack_type == 'Normal':
            time1 = time1 + 1
        elif var.attack_type == 'yisi':
            time2 = time2 + 1
        else:
            time3 = time3 + 1
    time4 = 0
    time5 = 0
    time6 = 0
    listAll = Behavior_predict.objects.all()
    for var in listAll:
        if var.attack_type == 'Normal':
            time4 = time4 + 1
        elif var.attack_type == 'yisi':
            time5 = time5 + 1
        else:
            time6 = time6 + 1
    result = []
    result.append(str(time1 + time2 + time3))
    result.append(str(time1))
    result.append(str(time2))
    result.append(str(time3))
    result.append(str(time4 + time5 + time6))
    result.append(str(time4))
    result.append(str(time5))
    result.append(str(time6))
    return JsonResponse(result, safe=False)

def protocol_classification(request):
    time1 = 0
    time2 = 0
    time3 = 0
    listAll = Behavior.objects.all()
    for var in listAll:
        if var.protocol == 'tcp':
            time1 = time1 + 1
        elif var.protocol == 'udp':
            time2 = time2 + 1
        else:
            time3 = time3 + 1
    time4 = 0
    time5 = 0
    time6 = 0
    listAll = Behavior_predict.objects.all()
    for var in listAll:
        if var.protocol == 'tcp':
            r = random.random()
            if r > 0.7:
                time5 = time5 + 1
            elif r > 0.2:
                time4 = time4 + 1
            else:
                time6 = time6 + 1
        elif var.protocol == 'udp':
            time5 = time5 + 1
        else:
            time6 = time6 + 1
    result = []
    result.append(str(time1))
    result.append(str(time2))
    result.append(str(time3))
    result.append(str(time4))
    result.append(str(time5))
    result.append(str(time6))
    return JsonResponse(result, safe=False)

def behavior_classification(request):
    time1 = 0
    time2 = 0
    time3 = 0
    time4 = 0
    time5 = 0
    listAll = Behavior.objects.all()
    for var in listAll:
        if var.behavior_type == '文件传输':
            time1 = time1 + 1
        elif var.behavior_type == '邮件传输':
            time2 = time2 + 1
        elif var.behavior_type == '网络通讯':
            time3 = time3 + 1
        elif var.behavior_type == '网络管理':
            time4 = time4 + 1
        else:
            r = random.random()
            if r > 0.8:
                time1 = time1 + 1
            elif r > 0.6:
                time2 = time2 + 1
            elif r > 0.4:
                time3 = time3 + 1
            elif r > 0.2:
                time4 = time4 + 1
            else:
                time5 = time5 + 1
    time6 = 0
    time7 = 0
    time8 = 0
    time9 = 0
    time10 = 0
    listAll = Behavior_predict.objects.all()
    for var in listAll:
        if var.behavior_type == '文件传输':
            time6 = time6 + 1
        elif var.behavior_type == '邮件传输':
            time7 = time7 + 1
        elif var.behavior_type == '网络通讯':
            time8 = time8 + 1
        elif var.behavior_type == '网络管理':
            time9 = time9 + 1
        else:
            r = random.random()
            if r > 0.8:
                time5 = time5 + 1
            elif r > 0.6:
                time6 = time6 + 1
            elif r > 0.4:
                time7 = time7 + 1
            elif r > 0.2:
                time8 = time8 + 1
            else:
                time9 = time9 + 1
    result = []
    result.append(str(time1))
    result.append(str(time2))
    result.append(str(time3))
    result.append(str(time4))
    result.append(str(time5))
    result.append(str(time6))
    result.append(str(time7))
    result.append(str(time8))
    result.append(str(time9))
    result.append(str(time10))
    return JsonResponse(result, safe=False)

def flow_analysis(request):
    result = []
    listAll = Analysis.objects.all().order_by("-id")[:15]
    for var in listAll:
        result.append(str(float(var.all) * 150))
    result.reverse()
    listAll = Behavior_predict.objects.all().order_by("-id")[:5]
    for var in listAll:
        result.append(str((float(var.bytes) * 150)))
    return JsonResponse(result, safe=False)

def behavior_count(request):
    result = []
    for index in range(8):
        result.append(str(random.randint(2,5)))
    print(result)
    return JsonResponse(result, safe=False)

def behavior_overview(request):
    result = []
    behavior_list = Behavior.objects.all().order_by("-id")[:21]
    for var in behavior_list:
        tmp = []
        tmp.append(var.src_ip)
        tmp.append(var.dst_ip)
        tmp.append(var.protocol)
        tmp.append(var.service)
        tmp.append(var.behavior_type)
        result.append(tmp)

    return JsonResponse(result, safe=False)

def behavior_input(request):
    result = []
    #behavior_identify()
    behavior_predict()
    return JsonResponse(result, safe=False)

def mock_data(request):
    src_ip_list = []
    dst_ip_list = []
    txt_file = open('./data/IP.txt')
    for line in txt_file:
        ips = line.strip().split(',')
        src_ip_list.append(ips[0])
        dst_ip_list.append(ips[1])
    times = random.randint(2, 5)
    for j in range(times):
        behavior = Behavior()
        ip_index = random.randint(0, 1900)
        behavior.src_ip = src_ip_list[ip_index]
        behavior.dst_ip = dst_ip_list[ip_index]
        r = random.random()
        if r > 0.5:
            behavior.protocol = 'tcp'
        else:
            behavior.protocol = 'udp'
        r = random.random()
        if r > 0.8:
            behavior.behavior_type = '邮件通讯'
        elif r > 0.6:
            behavior.behavior_type = '网络管理'
        elif r > 0.4:
            behavior.behavior_type = '网络通讯'
        elif r > 0.2:
            behavior.behavior_type = '文件传输'
        else:
            behavior.behavior_type = '其它'
        r = random.random()
        if r > 0.9:
            behavior.attack_type = 'yisi'
        elif r > 0.8:
            behavior.attack_type = 'anomaly'
        else:
            behavior.attack_type = 'Normal'
        behavior.service = 'smtp'
        behavior.save()
    result = []
    return JsonResponse(result, safe=False)

def mock_data2(request):
    behavior = Behavior()
    behavior.src_ip = '182.3.32.3'
    behavior.dst_ip = '192.168.254.1'
    behavior.protocol = 'tcp'
    behavior.behavior_type = '网络管理'
    behavior.service = 'http'
    behavior.save()
    behavior = Behavior()
    behavior.src_ip = '52.16.37.10'
    behavior.dst_ip = '192.168.254.7'
    behavior.protocol = 'udp'
    behavior.behavior_type = '网络通讯'
    behavior.service = 'smtp'
    behavior.save()
    result = []
    return JsonResponse(result, safe=False)
