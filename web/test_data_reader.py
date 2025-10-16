#!/usr/bin/env python3
"""
数据读取模块测试脚本
用于验证DataReader类的功能
"""
import os
import sys
import django

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

from model.data_reader import DataReader, DataProcessor

def test_data_reader():
    """测试DataReader类的基本功能"""
    print("=== 数据读取模块测试 ===")
    
    # 创建数据读取器实例
    data_reader = DataReader()
    
    # 测试数据源状态
    print("\n1. 数据源状态检查:")
    summary = data_reader.get_data_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # 测试文件验证
    print("\n2. 数据文件验证:")
    validation = data_reader.validate_data_paths()
    for file_type, exists in validation.items():
        status = "✓ 存在" if exists else "✗ 不存在"
        print(f"  {file_type}: {status}")
    
    # 测试Per-Flow数据读取
    print("\n3. Per-Flow数据读取测试:")
    perflow_data = data_reader.read_perflow_data(use_demo=False)
    if perflow_data:
        print(f"  成功读取 {len(perflow_data)} 条Per-Flow数据")
        if len(perflow_data) > 0:
            print(f"  示例数据: {perflow_data[0]}")
    else:
        print("  未读取到Per-Flow数据")
    
    # 测试TopK数据读取
    print("\n4. TopK数据读取测试:")
    topk_data = data_reader.read_topk_data(use_demo=False)
    if topk_data:
        print(f"  成功读取 {len(topk_data)} 条TopK数据")
        if len(topk_data) > 0:
            print(f"  示例数据: {topk_data[0]}")
    else:
        print("  未读取到TopK数据")
    
    # 测试分位数数据读取
    print("\n5. 分位数数据读取测试:")
    fenwei_data = data_reader.read_fenwei_data(use_demo=False)
    if fenwei_data:
        print(f"  成功读取 {len(fenwei_data)} 条分位数数据")
        if len(fenwei_data) > 0:
            print(f"  示例数据: {fenwei_data[0]}")
    else:
        print("  未读取到分位数数据")
    
    # 测试数据库数据读取
    print("\n6. 数据库数据读取测试:")
    analysis_data = data_reader.get_analysis_data_from_db()
    print(f"  数据库中有 {len(analysis_data)} 条分析数据")
    
    port_data = data_reader.get_port_info_from_db()
    print(f"  数据库中有 {len(port_data)} 条端口信息数据")
    
    print("\n=== 测试完成 ===")

def test_data_processor():
    """测试DataProcessor类的基本功能"""
    print("\n=== 数据处理模块测试 ===")
    
    data_reader = DataReader()
    analysis_data = data_reader.get_analysis_data_from_db()
    
    if analysis_data:
        print(f"  使用 {len(analysis_data)} 条分析数据进行处理测试")
        
        # 测试分析数据处理
        processed_data = DataProcessor.process_analysis_data(analysis_data, "ipv4")
        print(f"  处理后的IPv4数据: {processed_data}")
        
        # 测试端口数据处理
        port_data = data_reader.get_port_info_from_db()
        if port_data:
            processed_port_data = DataProcessor.process_port_data(port_data)
            print(f"  处理后的端口数据条数: {len(processed_port_data)}")
            if processed_port_data:
                print(f"  示例端口数据: {processed_port_data[0]}")
    else:
        print("  没有分析数据可供处理测试")
    
    print("\n=== 数据处理测试完成 ===")

if __name__ == "__main__":
    try:
        test_data_reader()
        test_data_processor()
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

