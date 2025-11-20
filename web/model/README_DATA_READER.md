# DataReader 使用说明

## 概述

`DataReader` 类是一个统一的数据读取接口，封装了所有数据读取逻辑，包括 CSV 文件、PCAP 文件和数据库查询。

## PCAP 文件读取

### 基本用法

```python
from model.data_reader import DataReader

# 创建 DataReader 实例
data_reader = DataReader()

# 读取 PCAP 文件并解析为流量五元组
flows = data_reader.read_pcap_flows()

# flows 是一个列表，每个元素包含：
# {
#     'src_ip': '源IP地址',
#     'dst_ip': '目的IP地址',
#     'src_port': 源端口号,
#     'dst_port': 目的端口号,
#     'protocol': '协议类型(TCP/UDP)',
#     'packet_count': 包数量,
#     'byte_count': 总字节数
# }
```

### 指定 PCAP 文件路径

```python
# 使用自定义路径
flows = data_reader.read_pcap_flows('/path/to/your/file.pcap')
```

### 在视图中使用

```python
from django.shortcuts import render
from model.data_reader import DataReader

def record(request):
    # 读取流量数据
    data_reader = DataReader()
    record_info = data_reader.read_pcap_flows()
    
    # 渲染模板
    return render(request, 'record.html', {'record': record_info})
```

## 配置 PCAP 文件路径

在 `config/data_config.py` 中配置 PCAP 文件路径：

```python
PCAP_FILES = {
    'test': os.path.join(PCAP_DATA_BASE, 'third', 'ceshi_000018.pcap'),
    'demo1': os.path.join(PCAP_DATA_BASE, 'third', 'ceshi_000018.pcap'),
}
```

## 其他数据读取方法

### Per-Flow 分析数据
```python
perflow_data = data_reader.read_perflow_data()
```

### TopK 分析数据
```python
topk_data = data_reader.read_topk_data(chunk_size=20)
```

### 分位数估计数据
```python
fenwei_data = data_reader.read_fenwei_data()
```

### 数据库查询
```python
# 获取所有分析数据
analysis_data = data_reader.get_analysis_data_from_db()

# 获取最新的分析数据
latest_data = data_reader.get_latest_analysis_data(limit=10)

# 获取端口信息
port_info = data_reader.get_port_info_from_db()
```

## 数据验证

```python
# 验证所有数据文件路径
validation_result = data_reader.validate_data_paths()

# 获取数据源摘要
summary = data_reader.get_data_summary()
```

## 优势

1. **统一接口**：所有数据读取逻辑集中在一个类中
2. **易于维护**：修改数据源只需修改 `data_reader.py` 和配置文件
3. **错误处理**：内置完善的错误处理和日志记录
4. **灵活配置**：通过配置文件轻松切换数据源
5. **类型安全**：使用类型提示，提高代码可读性

## 迁移说明

原来的 `db_url()` 函数已被 `DataReader.read_pcap_flows()` 替代：

**旧代码：**
```python
record_info = db_url(request)
```

**新代码：**
```python
from model.data_reader import DataReader
data_reader = DataReader()
record_info = data_reader.read_pcap_flows()
```
