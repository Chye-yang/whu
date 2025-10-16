#!/usr/bin/env python3
"""
测试修复后的数据配置
"""
import sys
import os

# 添加项目路径
sys.path.append('/home/whu/os/web')

try:
    from config.data_config import (
        get_data_path,
        get_domain_data_path,
        get_pcap_data_path,
        get_all_data_paths
    )
    
    print("=== 修复后的数据配置测试 ===")
    print()
    
    # 测试所有数据路径
    print("1. 测试所有数据路径配置:")
    all_paths = get_all_data_paths()
    for category, files in all_paths.items():
        print(f"   {category}:")
        for key, path in files.items():
            print(f"     {key}: {path}")
    print()
    
    # 测试domain数据路径
    print("2. 测试Domain数据路径:")
    try:
        domain_jiangsu = get_domain_data_path('domain_jiangsu')
        print(f"   ✓ domain_jiangsu: {domain_jiangsu}")
        
        domain_shandong = get_domain_data_path('domain_shandong')
        print(f"   ✓ domain_shandong: {domain_shandong}")
        
        ip_domain = get_domain_data_path('ip_domain')
        print(f"   ✓ ip_domain: {ip_domain}")
        
        globle = get_domain_data_path('globle')
        print(f"   ✓ globle: {globle}")
        
    except Exception as e:
        print(f"   ✗ Domain数据路径错误: {e}")
    print()
    
    # 测试pcap数据路径
    print("3. 测试PCAP数据路径:")
    try:
        test_pcap = get_pcap_data_path('test')
        print(f"   ✓ test: {test_pcap}")
        
        demo1_pcap = get_pcap_data_path('demo1')
        print(f"   ✓ demo1: {demo1_pcap}")
        
    except Exception as e:
        print(f"   ✗ PCAP数据路径错误: {e}")
    print()
    
    # 测试通用函数
    print("4. 测试通用get_data_path函数:")
    try:
        demo_csv = get_data_path('demo', 'csv')
        print(f"   ✓ demo/csv: {demo_csv}")
        
        domain_jiangsu = get_data_path('domain', 'domain_jiangsu')
        print(f"   ✓ domain/domain_jiangsu: {domain_jiangsu}")
        
        pcap_test = get_data_path('pcap', 'test')
        print(f"   ✓ pcap/test: {pcap_test}")
        
    except Exception as e:
        print(f"   ✗ 通用函数错误: {e}")
    print()
    
    print("测试完成！Domain和Record页面现在应该可以正常使用了。")
    
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在正确的目录下运行此脚本")
except Exception as e:
    print(f"测试过程中出现错误: {e}")



