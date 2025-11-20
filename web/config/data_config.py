"""
数据配置文件
定义演示数据源路径和配置参数
"""
import os
from django.conf import settings

# 演示数据基础路径
DEMO_DATA_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'analysis')

# Domain数据基础路径
DOMAIN_DATA_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'domain')

# PCAP数据基础路径
PCAP_DATA_BASE = os.path.join(os.path.dirname(settings.BASE_DIR), 'Data', 'OriginPcap')

# =============================
# 演示数据文件配置
# =============================
DEMO_FILES = {
    'csv': os.path.join(DEMO_DATA_BASE, 'inputCSV5.csv'),
    'perflow': os.path.join(DEMO_DATA_BASE, 'perflow_beijing-3.csv'),
    'topk': os.path.join(DEMO_DATA_BASE, 'topk_beijing-3.csv'),
    'fenwei': os.path.join(DEMO_DATA_BASE, 'fen.csv'),
    'result': os.path.join(DEMO_DATA_BASE, 'result.csv'),
}

# =============================
# Domain数据文件配置
# =============================
DOMAIN_FILES = {
    'domain_jiangsu': os.path.join(DOMAIN_DATA_BASE, 'Domain_JiangSu.csv'),
    'domain_shandong': os.path.join(DOMAIN_DATA_BASE, 'Domain_ShanDong.csv'),
    'ip_domain': os.path.join(DOMAIN_DATA_BASE, 'IP_domain.csv'),
    'globle': os.path.join(DOMAIN_DATA_BASE, 'globle.csv'),
}

# =============================
# PCAP数据文件配置
# =============================
PCAP_FILES = {
    'test': os.path.join(PCAP_DATA_BASE, 'third', 'ceshi_000018.pcap'),  # 默认测试文件
    'demo1': os.path.join(PCAP_DATA_BASE, 'third', 'ceshi_000018.pcap'),
    # 备用路径：os.path.join(PCAP_DATA_BASE, 'second', 'ceshi_815.pcap')
}

# =============================
# 简化的数据路径配置
# =============================
DATA_PATHS = {
    'demo': DEMO_FILES,
    'domain': DOMAIN_FILES,
    'pcap': PCAP_FILES,
}
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
        category: 数据类别 ('demo', 'domain', 'pcap')
        key: 数据键名
            - demo: csv, perflow, topk, fenwei, result
            - domain: domain_jiangsu, domain_shandong, ip_domain, globle
            - pcap: test, demo1
        
    Returns:
        数据文件完整路径
    """
    if category not in DATA_PATHS:
        raise ValueError(f"Unknown data category: {category}. Supported: {list(DATA_PATHS.keys())}")
    
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

def get_demo_data_path(key: str) -> str:
    """
    获取演示数据文件路径（便捷方法）
    
    Args:
        key: 数据键名 (csv, perflow, topk, fenwei, result)
        
    Returns:
        数据文件完整路径
    """
    return get_data_path('demo', key)

def get_domain_data_path(key: str) -> str:
    """
    获取Domain数据文件路径（便捷方法）
    
    Args:
        key: 数据键名 (domain_jiangsu, domain_shandong, ip_domain, globle)
        
    Returns:
        数据文件完整路径
    """
    return get_data_path('domain', key)

def get_pcap_data_path(key: str) -> str:
    """
    获取PCAP数据文件路径（便捷方法）
    
    Args:
        key: 数据键名 (test, demo1)
        
    Returns:
        数据文件完整路径
    """
    return get_data_path('pcap', key)

