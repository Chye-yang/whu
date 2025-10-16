#!/usr/bin/env python3
"""
测试Per-Flow数据源配置
"""
import sys
import os

# 添加项目路径
sys.path.append('/home/whu/os/web')

try:
    from config.data_config import (
        get_perflow_source_info, 
        switch_perflow_data_source,
        get_current_perflow_source,
        get_data_path
    )
    
    print("=== Per-Flow数据源配置测试 ===")
    print()
    
    # 显示当前配置信息
    info = get_perflow_source_info()
    print("当前数据源信息:")
    print(f"  当前使用: {info['current']}")
    print(f"  当前文件: {info['current_file']}")
    print()
    
    print("可用的数据源:")
    for key, desc in info['available'].items():
        print(f"  {key}: {desc}")
    print()
    
    # 测试切换功能
    print("测试数据源切换:")
    for source in ['perflow_beijing', 'perflow_original', 'perflow_changzhou']:
        if switch_perflow_data_source(source):
            current_path = get_data_path('changzhou', 'perflow')
            print(f"  ✓ 切换到 {source}: {current_path}")
        else:
            print(f"  ✗ 切换失败: {source}")
    
    print()
    print("测试完成！")
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在正确的目录下运行此脚本")
except Exception as e:
    print(f"测试过程中出现错误: {e}")


