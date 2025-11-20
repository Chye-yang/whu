#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换脚本：将perflow_beijing2.csv转换为expanded_selected_columns.csv格式
提取srcip、dstip、port、proto列并保存为topk_beijing.csv
"""

import pandas as pd
import os

def convert_perflow_to_topk():
    """
    将perflow_beijing2.csv转换为topk_beijing.csv格式
    """
    # 输入和输出文件路径
    input_file = "/home/whu/os/Data/analysis/perflow_beijing-3.csv"
    output_file = "/home/whu/os/Data/analysis/topk_beijing-3.csv"
    
    try:
        # 读取原始CSV文件
        print(f"正在读取文件: {input_file}")
        df = pd.read_csv(input_file)
        
        print(f"原始数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        # 检查必需的列是否存在
        required_columns = ['srcip', 'dstip', 'port', 'proto']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"错误: 缺少以下列: {missing_columns}")
            return False
        
        # 提取需要的列
        print("正在提取srcip、dstip、port、proto列...")
        selected_df = df[required_columns].copy()
        
        # 检查数据
        print(f"提取后数据形状: {selected_df.shape}")
        print(f"前5行数据:")
        print(selected_df.head())
        
        # 保存为新的CSV文件
        print(f"正在保存到: {output_file}")
        selected_df.to_csv(output_file, index=False, header=False)
        
        print(f"转换完成! 输出文件: {output_file}")
        print(f"共处理了 {len(selected_df)} 行数据")
        
        return True
        
    except FileNotFoundError:
        print(f"错误: 找不到输入文件 {input_file}")
        return False
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = convert_perflow_to_topk()
    if success:
        print("转换成功完成!")
    else:
        print("转换失败!")
