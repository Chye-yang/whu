# 数据读取模块重构说明

## 概述

本次重构将原本分散在 `analysis.py` 中的数据读取逻辑提取出来，创建了专门的数据读取模块，使代码结构更加清晰，便于维护和扩展。

## 新增文件

### 1. `model/data_reader.py`
专门的数据读取模块，包含以下主要类：

#### DataReader 类
- **功能**: 封装所有数据读取逻辑
- **主要方法**:
  - `read_perflow_data()`: 读取Per-Flow分析数据
  - `read_topk_data()`: 读取TopK分析数据
  - `read_fenwei_data()`: 读取分位数估计数据
  - `get_analysis_data_from_db()`: 从数据库获取分析数据
  - `get_port_info_from_db()`: 从数据库获取端口信息
  - `validate_data_paths()`: 验证数据文件路径
  - `get_data_summary()`: 获取数据源摘要信息

#### DataProcessor 类
- **功能**: 数据处理和加工
- **主要方法**:
  - `process_analysis_data()`: 处理分析数据，计算统计信息
  - `process_port_data()`: 处理端口数据

### 2. `config/data_config.py`
数据配置文件，统一管理：
- 数据文件路径配置
- 数据处理参数
- 数据库配置
- 日志配置

### 3. `test_data_reader.py`
测试脚本，用于验证数据读取模块的功能

## 修改的文件

### `model/analysis.py`
- 重构了所有视图函数，使用新的数据读取模块
- 添加了完善的错误处理
- 新增了数据状态和验证接口

#### 主要变更：
- `table1()`: Per-Flow分析数据接口
- `table2()`: Heavy Flow检测数据接口
- `table3()`: 分位数估计数据接口
- `table4()`: 网络层分析数据接口
- `mainTop()`: 主要统计数据接口
- `mainBottom()`: 实时流量分析数据接口
- `data_status()`: 数据源状态接口（新增）
- `data_validation()`: 数据文件验证接口（新增）

## 使用方式

### 基本使用
```python
from model.data_reader import DataReader

# 创建数据读取器
data_reader = DataReader()

# 读取Per-Flow数据
perflow_data = data_reader.read_perflow_data(use_demo=False)

# 读取TopK数据
topk_data = data_reader.read_topk_data(use_demo=False)

# 验证数据文件
validation = data_reader.validate_data_paths()
```

### 在视图函数中使用
```python
def table1(request):
    """Per-Flow分析数据接口"""
    try:
        data_reader = DataReader()
        result = data_reader.read_perflow_data(use_demo=False)
        
        if not result:
            return JsonResponse({"error": "No perflow data available"}, status=500)
            
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        return JsonResponse({"error": f"Failed to load perflow data: {str(e)}"}, status=500)
```

## 配置说明

### 数据文件路径配置
在 `config/data_config.py` 中配置各种数据文件的路径：

```python
DATA_PATHS = {
    'changzhou': {
        'perflow': 'path/to/perflow0524.csv',
        'topk': 'path/to/topk0524.csv',
        'fenwei': 'path/to/fenwei0524.csv',
    },
    'demo': {
        'csv': 'path/to/demo.csv',
        'perflow': 'path/to/demo_perflow.csv',
    }
}
```

### 数据处理参数配置
```python
DATA_PROCESSING_CONFIG = {
    'chunk_size': 20,  # CSV分块读取大小
    'scale_factor': 0.1,  # 数据缩放因子
    'max_display_rows': 10,  # 最大显示行数
    'update_interval': 1000,  # 数据更新间隔(毫秒)
}
```

## 错误处理

所有数据读取方法都包含完善的错误处理：
- 文件不存在检查
- 数据格式验证
- 异常捕获和日志记录
- 友好的错误信息返回

## 日志记录

使用Python标准logging模块记录：
- 数据读取成功/失败信息
- 文件路径验证结果
- 异常详细信息

## 测试

运行测试脚本验证功能：
```bash
cd /home/whu/os/web
python test_data_reader.py
```

## 优势

1. **代码分离**: 数据读取逻辑与业务逻辑分离
2. **易于维护**: 统一的数据读取接口
3. **配置灵活**: 通过配置文件管理数据路径
4. **错误处理**: 完善的异常处理机制
5. **可扩展性**: 易于添加新的数据源
6. **可测试性**: 独立的测试脚本

## 注意事项

1. 确保数据文件路径正确配置
2. 数据库连接正常
3. 相关依赖包已安装
4. 日志目录有写入权限

## 后续扩展

可以进一步扩展的功能：
- 支持更多数据格式（JSON、XML等）
- 数据缓存机制
- 数据预处理管道
- 实时数据流处理
- 数据质量监控

