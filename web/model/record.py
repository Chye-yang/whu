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

def record_speed(request):
    result = []
    for index in range(5):
        result.append(str(random.randint(500,700)))
    return JsonResponse(result, safe=False)


def record_ping(request):
    result = []
    for index in range(5):
        result.append(str(random.uniform(90, 100)))  # 使用 random.uniform 生成浮点数
    return JsonResponse(result, safe=False)