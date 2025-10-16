"""
数据读取模块
专门负责从各种数据源读取数据，包括CSV文件、数据库等
"""
import pandas as pd
import csv
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter
from django.conf import settings
from .db import Analysis, PortInfo

# 导入数据配置
try:
    from config.data_config import get_data_path, get_processing_config, get_database_config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    def get_data_path(category, key):
        return os.path.join(settings.BASE_DIR, 'data', f"{category}/{key}")
    
    def get_processing_config():
        return {'chunk_size': 20, 'scale_factor': 0.1, 'max_display_rows': 10}
    
    def get_database_config():
        return {}

# 配置日志
logger = logging.getLogger(__name__)

class DataReader:
    """数据读取器类，封装所有数据读取逻辑"""
    
    def __init__(self, base_data_path: str = None):
        """
        初始化数据读取器
        
        Args:
            base_data_path: 数据文件基础路径，默认为项目根目录下的data文件夹
        """
        if base_data_path is None:
            self.base_data_path = os.path.join(settings.BASE_DIR, 'data')
        else:
            self.base_data_path = base_data_path
        
        # 获取配置
        self.processing_config = get_processing_config()
        
        # 数据文件路径配置（只使用demo数据）
        self.data_paths = {
            'csv': get_data_path('demo', 'csv'),
            'perflow': get_data_path('demo', 'perflow'),
            'topk': get_data_path('demo', 'topk'),
            'fenwei': get_data_path('demo', 'fenwei'),
            'result': get_data_path('demo', 'result'),
        }
    
    def _check_file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return False
        return True
    
    def _safe_read_csv(self, file_path: str, **kwargs) -> Optional[pd.DataFrame]:
        """
        安全读取CSV文件或Excel文件
        
        Args:
            file_path: 文件路径
            **kwargs: pandas读取方法的其他参数
            
        Returns:
            DataFrame或None（如果读取失败）
        """
        try:
            if not self._check_file_exists(file_path):
                return None
            
            # 检查文件扩展名，如果是Excel文件则使用read_excel
            if file_path.lower().endswith(('.xlsx', '.xls')) or self._is_excel_file(file_path):
                df = pd.read_excel(file_path, **kwargs)
                logger.info(f"成功读取Excel文件: {file_path}, 行数: {len(df)}")
            else:
                df = pd.read_csv(file_path, **kwargs)
                logger.info(f"成功读取CSV文件: {file_path}, 行数: {len(df)}")
            
            return df
            
        except pd.errors.EmptyDataError:
            logger.error(f"文件为空: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    def _is_excel_file(self, file_path: str) -> bool:
        """
        检查文件是否为Excel格式
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为Excel文件
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                # 检查Excel文件头
                return header.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1') or \
                       header.startswith(b'PK\x03\x04')  # .xlsx文件头
        except:
            return False
    
    def read_perflow_data(self) -> List[List[Any]]:
        """
        读取Per-Flow分析数据
        
        Returns:
            Per-Flow数据列表
        """
        file_path = self.data_paths['perflow']
        
        df = self._safe_read_csv(file_path)
        if df is None:
            return []
        
        result = []
        try:
            for index, row in df.iterrows():
                result.append([
                    row[0],   # 流ID
                    row[45],  # 源IP
                    row[46],  # 目的IP
                    row[47],  # 源端口号
                    row[2],   # 协议类型
                    row[7],   # 包大小
                ])
        except Exception as e:
            logger.error(f"处理Per-Flow数据时出错: {str(e)}")
            return []
        
        return result
    
    def read_topk_data(self, chunk_size: int = None) -> List[Dict[str, Any]]:
        """
        读取TopK分析数据
        
        Args:
            chunk_size: 分块读取大小，如果为None则使用配置中的默认值
            
        Returns:
            TopK数据列表
        """
        if chunk_size is None:
            chunk_size = self.processing_config.get('chunk_size', 20)
            
        file_path = self.data_paths['topk']
        
        if not self._check_file_exists(file_path):
            return []
        
        counter = Counter()
        result = []
        
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                while True:
                    chunk = [next(csv_reader, None) for _ in range(chunk_size)]
                    chunk = [row for row in chunk if row]
                    if not chunk:
                        break
                    
                    counter.update(tuple(row) for row in chunk)
                    top_items = counter.most_common(45)
                    
                    for rank, (row, count) in enumerate(top_items, start=1):
                        result.append({"rank": rank, "row": row, "count": count})
                        
        except Exception as e:
            logger.error(f"读取TopK数据时出错: {str(e)}")
            return []
        
        return result
    
    def read_fenwei_data(self) -> List[List[Any]]:
        """
        读取分位数估计数据
        
        Returns:
            分位数数据列表
        """
        file_path = self.data_paths['fenwei']
        
        df = self._safe_read_csv(file_path)
        if df is None:
            return []
        
        result = []
        try:
            for index, row in df.iterrows():
                # 安全转换数值类型
                value4 = int(row[4]) if isinstance(row[4], (int, float)) else row[4]
                value5 = int(row[5]) if isinstance(row[5], (int, float)) else row[5]
                value6 = int(row[6]) if isinstance(row[6], (int, float)) else row[6]
                
                result.append([
                    row[0],   # 源IP
                    row[1],   # 目的IP
                    row[2],   # 端口号
                    row[3],   # 协议类型
                    value4,   # 25%分位数
                    value5,   # 50%分位数
                    value6,   # 75%分位数
                ])
        except Exception as e:
            logger.error(f"处理分位数数据时出错: {str(e)}")
            return []
        
        return result
    
    def read_csv_data(self) -> Optional[pd.DataFrame]:
        """
        读取CSV数据
        
        Returns:
            CSV数据DataFrame
        """
        return self._safe_read_csv(self.data_paths['csv'])
    
    def get_analysis_data_from_db(self) -> List[Analysis]:
        """
        从数据库获取分析数据
        
        Returns:
            Analysis对象列表
        """
        try:
            return list(Analysis.objects.all())
        except Exception as e:
            logger.error(f"从数据库获取分析数据失败: {str(e)}")
            return []
    
    def get_port_info_from_db(self) -> List[PortInfo]:
        """
        从数据库获取端口信息
        
        Returns:
            PortInfo对象列表
        """
        try:
            return list(PortInfo.objects.all())
        except Exception as e:
            logger.error(f"从数据库获取端口信息失败: {str(e)}")
            return []
    
    def get_latest_analysis_data(self, limit: int = 10) -> List[Analysis]:
        """
        获取最新的分析数据
        
        Args:
            limit: 限制返回的记录数
            
        Returns:
            最新的Analysis对象列表
        """
        try:
            return list(Analysis.objects.all().order_by("-id")[:limit])
        except Exception as e:
            logger.error(f"获取最新分析数据失败: {str(e)}")
            return []
    
    def get_top_ports_by_cur(self, limit: int = 11) -> List[PortInfo]:
        """
        按当前流量获取前N个端口
        
        Args:
            limit: 限制返回的记录数
            
        Returns:
            按流量排序的PortInfo对象列表
        """
        try:
            return list(PortInfo.objects.all().order_by("-cur")[:limit])
        except Exception as e:
            logger.error(f"获取端口流量排序数据失败: {str(e)}")
            return []
    
    def validate_data_paths(self) -> Dict[str, bool]:
        """
        验证所有数据文件路径是否存在
        
        Returns:
            文件路径存在性字典
        """
        validation_result = {}
        for key, path in self.data_paths.items():
            validation_result[key] = self._check_file_exists(path)
        return validation_result
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        获取数据源摘要信息
        
        Returns:
            数据源摘要字典
        """
        summary = {
            'base_path': self.base_data_path,
            'file_validation': self.validate_data_paths(),
            'db_analysis_count': Analysis.objects.count(),
            'db_port_count': PortInfo.objects.count(),
        }
        return summary


class DataProcessor:
    """数据处理类，负责对读取的数据进行加工处理"""
    
    @staticmethod
    def process_analysis_data(analysis_list: List[Analysis], param: str) -> List[str]:
        """
        处理分析数据，计算统计信息
        
        Args:
            analysis_list: Analysis对象列表
            param: 要处理的参数字段名
            
        Returns:
            处理后的数据列表
        """
        try:
            str_list = list(Analysis.objects.values_list(param))
            float_list = [float(var[0]) for var in str_list]
            
            result_list = []
            if not str_list:
                result_list.append("0.00TB")
            elif str_list[-1][0] == 0:
                result_list.append("0.00TB")
            else:
                result_list.append(str(float("%.3g" % float(str_list[-1][0]))) + "TB")
            
            if not float_list:
                result_list.extend(["0.00TB"] * 5)
            else:
                import numpy as np
                result_list.append(str(float("%.3g" % np.mean(float_list))) + "TB")
                result_list.append(str(float("%.3g" % np.max(float_list))) + "TB")
                result_list.append(str(float("%.3g" % np.min(float_list))) + "TB")
                result_list.append(str(float("%.3g" % np.sum(float_list))) + "TB")
                result_list.append(str(float("%.3g" % np.std(float_list))))
            
            result_list.append(str(param))
            return result_list
            
        except Exception as e:
            logger.error(f"处理分析数据时出错: {str(e)}")
            return ["0.00TB"] * 6
    
    @staticmethod
    def process_port_data(port_list: List[PortInfo]) -> List[List[str]]:
        """
        处理端口数据
        
        Args:
            port_list: PortInfo对象列表
            
        Returns:
            处理后的端口数据列表
        """
        try:
            import numpy as np
            import random
            
            float_list_all = [float(var.cur) for var in port_list]
            float_list_in = [float(var.inFlow) for var in port_list]
            float_list_out = [float(var.outFlow) for var in port_list]
            
            sum_all = np.sum(float_list_all)
            sum_in = np.sum(float_list_in)
            sum_out = np.sum(float_list_out)
            
            result = []
            for var in port_list:
                tmp = []
                tmp.append(str(var.no))
                xy = float(var.cur) + float(random.randint(-1, 40) / 3)
                tmp.append(str(float("%.3g" % float(xy))) + "MB")
                tmp.append(str(float("%.4g" % (float(var.cur) / float(sum_all) * 100))) + "%")
                tmp.append(str(float("%.3g" % float(var.inFlow))) + "MB")
                tmp.append(str(float("%.4g" % (float(var.inFlow) / float(sum_in) * 100))) + "%")
                tmp.append(str(float("%.3g" % float(var.outFlow))) + "MB")
                tmp.append(str(float("%.4g" % (float(var.outFlow) / float(sum_out) * 100))) + "%")
                
                if xy > float(var.pre):
                    tmp.append("上升")
                elif xy == float(var.pre):
                    tmp.append("不变")
                else:
                    tmp.append("下降")
                
                result.append(tmp)
            
            return result
            
        except Exception as e:
            logger.error(f"处理端口数据时出错: {str(e)}")
            return []
