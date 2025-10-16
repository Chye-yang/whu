"""
数据配置文件
定义各种数据源路径和配置参数

Per-Flow数据源切换说明:
1. 修改 PERFLOW_DATA_SOURCE 变量来切换数据源:
   - 'perflow_beijing': 使用 perflow_beijing.csv (默认)
   - 'perflow_original': 使用 perflow.csv
   - 'perflow_changzhou': 使用 perflow0524.csv

2. 或者使用函数动态切换:
   from config.data_config import switch_perflow_data_source
   switch_perflow_data_source('perflow_beijing')

3. 查看当前数据源信息:
   from config.data_config import get_perflow_source_info
   print(get_perflow_source_info())
"""
import os
from django.conf import settings

# 数据文件基础路径
BASE_DATA_PATH = os.path.join(settings.BASE_DIR, 'data')

# =============================
# 数据源切换配置
# =============================
# Per-Flow分析数据源选择
# 可选值: 'perflow_beijing', 'perflow_original', 'perflow_changzhou'
PERFLOW_DATA_SOURCE = 'perflow_beijing'  # 默认使用perflow_beijing.csv

# domain 页面数据（相对路径迁移后目录）
DOMAIN_EXTERNAL_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'domain')

# analysis 页面演示数据（相对路径迁移后目录）
ANALYSIS_EXTERNAL_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'analysis')

# pcap 外部数据目录（迁移后目录）
PCAP_EXTERNAL_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'OriginPcap')

# =============================
# analysis.html 所需数据文件
# =============================
ANALYSIS_FILES = {
    # 演示/分析页 CSV
    'csv': os.path.join(ANALYSIS_EXTERNAL_BASE, 'inputCSV5.csv'),
    'perflow': os.path.join(ANALYSIS_EXTERNAL_BASE, 'perflow_beijing.csv'),
    'topk': os.path.join(ANALYSIS_EXTERNAL_BASE, 'expanded_selected_columns.csv'),
    'fenwei': os.path.join(ANALYSIS_EXTERNAL_BASE, 'fenweishu.csv'),
    'result': os.path.join(ANALYSIS_EXTERNAL_BASE, 'result.csv'),

    # 常州数据（历史路径保留，供需要时使用）
    'cz_perflow0524': os.path.join(BASE_DATA_PATH, 'ChangZhouData/0524/Result/perflow0524.csv'),
    'cz_topk0524': os.path.join(BASE_DATA_PATH, 'ChangZhouData/0524/Result/topk0524.csv'),
    'cz_fenwei0524': os.path.join(BASE_DATA_PATH, 'ChangZhouData/0524/Result/fenwei0524.csv'),
    
    # 其他可用的perflow数据源
    'perflow_original': os.path.join(ANALYSIS_EXTERNAL_BASE, 'perflow.csv'),
    'perflow_changzhou': os.path.join(BASE_DATA_PATH, 'ChangZhouData/0524/Result/perflow0524.csv'),
}

# =============================
# domain 页面所需数据文件
# =============================
DOMAIN_FILES = {
    'domain_jiangsu': os.path.join(DOMAIN_EXTERNAL_BASE, 'Domain_JiangSu.csv'),
    'domain_shandong': os.path.join(DOMAIN_EXTERNAL_BASE, 'Domain_ShanDong.csv'),
    'ip_domain': os.path.join(DOMAIN_EXTERNAL_BASE, 'IP_domain.csv'),
    'globle': os.path.join(DOMAIN_EXTERNAL_BASE, 'globle.csv'),
}

# =============================
# record 页面所需数据文件（PCAP）
# =============================
RECORD_FILES = {
    # 与现有代码 get_data_path('changzhou','cut0524') 一致的默认来源
    'cut0524': os.path.join(PCAP_EXTERNAL_BASE, 'ceshi_000022.pcap'),

    # 备用样例（可按需切换）
    'alt_000022': os.path.join(PCAP_EXTERNAL_BASE, 'ceshi_000022.pcap'),
}

# =============================
# 兼容旧结构：DATA_PATHS 与 get_data_path 保留
# =============================
# 根据配置选择perflow数据源
def get_perflow_data_source():
    """根据PERFLOW_DATA_SOURCE配置返回对应的数据源"""
    source_mapping = {
        'perflow_beijing': 'perflow',
        'perflow_original': 'perflow_original', 
        'perflow_changzhou': 'perflow_changzhou'
    }
    return source_mapping.get(PERFLOW_DATA_SOURCE, 'perflow')

DATA_PATHS = {
    'changzhou': {
        'perflow': ANALYSIS_FILES[get_perflow_data_source()],  # 动态选择perflow数据源
        'topk': ANALYSIS_FILES['cz_topk0524'],
        'fenwei': ANALYSIS_FILES['cz_fenwei0524'],
        'cut0524': RECORD_FILES['cut0524'],
        'domain_jiangsu': DOMAIN_FILES['domain_jiangsu'],
        'domain_shandong': DOMAIN_FILES['domain_shandong'],
        'ip_domain': DOMAIN_FILES['ip_domain'],
        'globle': DOMAIN_FILES['globle'],
    },
    'demo': {
        'csv': ANALYSIS_FILES['csv'],
        'perflow': ANALYSIS_FILES['perflow'],
        'topk': ANALYSIS_FILES['topk'],
        'fenwei': ANALYSIS_FILES['fenwei'],
        'result': ANALYSIS_FILES['result'],
    },
    'pcap': {
        'test': os.path.join(BASE_DATA_PATH, 'demoPcap/test.pcap'),
        'demo1': os.path.join(BASE_DATA_PATH, 'demoPcap/1.pcap'),
        'demo2': os.path.join(BASE_DATA_PATH, 'demoPcap/2.pcap'),
        'demo3': os.path.join(BASE_DATA_PATH, 'demoPcap/3.pcap'),
    },
    'models': {
        'decision_tree': os.path.join(BASE_DATA_PATH, 'demoCSV/DecisionTreeClassifier.pkl'),
        'lstm_model1': os.path.join(BASE_DATA_PATH, 'demoCSV/lstm-model.h5'),
        'lstm_model2': os.path.join(BASE_DATA_PATH, 'demoCSV/lstm-model2.h5'),
        'lstm_model3': os.path.join(BASE_DATA_PATH, 'demoCSV/lstm-model3.h5'),
    }
}

# 数据处理参数
DATA_PROCESSING_CONFIG = {
    'chunk_size': 20,  # CSV分块读取大小
    'scale_factor': 0.1,  # 数据缩放因子
    'max_display_rows': 10,  # 最大显示行数
    'update_interval': 1000,  # 数据更新间隔(毫秒)
}

# 数据库配置
DATABASE_CONFIG = {
    'analysis_table': 'analysis',
    'port_info_table': 'portinfo',
    'record_table': 'netlog',
    'statistic_table': 'tiny-set',
    'behavior_table': 'behavior',
    'behavior_predict_table': 'behavior_predict',
    'prediction_table': 'model_prediction',
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join(settings.BASE_DIR, 'logs', 'data_reader.log'),
}

def get_data_path(category: str, key: str) -> str:
    """
    获取数据文件路径
    
    Args:
        category: 数据类别 (changzhou, demo, pcap, models)
        key: 数据键名
        
    Returns:
        数据文件完整路径
    """
    if category not in DATA_PATHS:
        raise ValueError(f"Unknown data category: {category}")
    
    if key not in DATA_PATHS[category]:
        raise ValueError(f"Unknown data key: {key} in category: {category}")
    
    return DATA_PATHS[category][key]

def get_all_data_paths() -> dict:
    """获取所有数据路径配置"""
    return DATA_PATHS

def get_processing_config() -> dict:
    """获取数据处理配置"""
    return DATA_PROCESSING_CONFIG

def get_database_config() -> dict:
    """获取数据库配置"""
    return DATABASE_CONFIG

def switch_perflow_data_source(source: str) -> bool:
    """
    切换Per-Flow数据源
    
    Args:
        source: 数据源名称 ('perflow_beijing', 'perflow_original', 'perflow_changzhou')
        
    Returns:
        bool: 切换是否成功
    """
    global PERFLOW_DATA_SOURCE
    valid_sources = ['perflow_beijing', 'perflow_original', 'perflow_changzhou']
    
    if source in valid_sources:
        PERFLOW_DATA_SOURCE = source
        return True
    else:
        print(f"无效的数据源: {source}. 有效选项: {valid_sources}")
        return False

def get_current_perflow_source() -> str:
    """获取当前使用的Per-Flow数据源"""
    return PERFLOW_DATA_SOURCE

def get_perflow_source_info() -> dict:
    """获取所有可用的Per-Flow数据源信息"""
    return {
        'current': PERFLOW_DATA_SOURCE,
        'available': {
            'perflow_beijing': '北京数据 (perflow_beijing.csv)',
            'perflow_original': '原始数据 (perflow.csv)', 
            'perflow_changzhou': '常州数据 (perflow0524.csv)'
        },
        'current_file': ANALYSIS_FILES[get_perflow_data_source()]
    }

