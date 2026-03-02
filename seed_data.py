#!/usr/bin/env python
"""
种子数据脚本 - 为库尔勒香梨生产溯源管理系统生成演示数据
确保所有数据都对齐到2026年1月至2月，并正确处理外键关系
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KorlaPearTraceabilitySystem.settings')
django.setup()

from homepage.models import Employees, Crops, Livestock, Machinery, Milk_production, Eggs_production
from django.contrib.auth.models import User

def create_seed_data():
    print("=" * 70)
    print("开始生成库尔勒香梨生产溯源管理系统演示数据")
    print("=" * 70)
    
    # 1. 确保admin用户存在
    print("\n1. 创建/验证管理员用户...")
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', '123456')
        print("   ✓ 创建管理员用户: admin/123456")
    else:
        admin_user = User.objects.get(username='admin')
        print("   ✓ 管理员用户已存在")
    
    # 2. 创建员工数据
    print("\n2. 创建员工数据...")
    employees_data = [
        {'Eid': 1001, 'Name': '张伟', 'Country_code': '+86', 'Phone_number': '13800138001', 
         'Position': '技术主管', 'Salary': 15000, 'Performance': '优秀'},
        {'Eid': 1002, 'Name': '阿依古丽', 'Country_code': '+86', 'Phone_number': '13800138002', 
         'Position': '采摘组长', 'Salary': 12000, 'Performance': '良好'},
        {'Eid': 1003, 'Name': '王强', 'Country_code': '+86', 'Phone_number': '13800138003', 
         'Position': '物流司机', 'Salary': 10000, 'Performance': '良好'},
        {'Eid': 1004, 'Name': '李娜', 'Country_code': '+86', 'Phone_number': '13800138004', 
         'Position': '质检员', 'Salary': 11000, 'Performance': '优秀'},
        {'Eid': 1005, 'Name': '买买提', 'Country_code': '+86', 'Phone_number': '13800138005', 
         'Position': '果园管理员', 'Salary': 13000, 'Performance': '良好'},
    ]
    
    employees_created = 0
    for emp in employees_data:
        if not Employees.objects.filter(Eid=emp['Eid']).exists():
            Employees.objects.create(user=admin_user, **emp)
            employees_created += 1
            print(f"   ✓ 创建员工: {emp['Name']} ({emp['Position']})")
    
    print(f"   总计: {Employees.objects.filter(user=admin_user).count()} 名员工")
    
    # 3. 创建种植档案数据（地块）
    print("\n3. 创建种植档案数据...")
    crops_data = [
        {'Cid': 2001, 'Field_name': '阿瓦提乡1号地块', 
         'Field_description': '优质香梨种植地块，50亩，土壤肥沃，灌溉设施完善', 
         'Crop_name': '库尔勒香梨', 'Variety': '香梨', 
         'Planting_date': '2023-03-01', 'Is_harvested': True, 'Harvesting_date': '2023-09-15'},
        {'Cid': 2002, 'Field_name': '铁门关2号示范林', 
         'Field_description': '现代化种植技术，120亩，采用滴灌系统，有机种植', 
         'Crop_name': '库尔勒香梨', 'Variety': '香梨', 
         'Planting_date': '2023-03-05', 'Is_harvested': True, 'Harvesting_date': '2023-09-20'},
        {'Cid': 2003, 'Field_name': '库尔勒市郊3号果园', 
         'Field_description': '新开发果园，80亩，2024年新种植', 
         'Crop_name': '库尔勒香梨', 'Variety': '香梨', 
         'Planting_date': '2024-03-10', 'Is_harvested': False, 'Harvesting_date': None},
    ]
    
    crops_created = 0
    for crop in crops_data:
        if not Crops.objects.filter(Cid=crop['Cid']).exists():
            Crops.objects.create(user=admin_user, **crop)
            crops_created += 1
            print(f"   ✓ 创建种植档案: {crop['Field_name']}")
    
    print(f"   总计: {Crops.objects.filter(user=admin_user).count()} 个种植地块")
    
    # 4. 创建采摘批次数据（与地块关联）
    print("\n4. 创建采摘批次数据...")
    
    # 获取已收获的地块
    harvested_crops = Crops.objects.filter(user=admin_user, Is_harvested=True)
    
    # 为每个已收获的地块创建采摘批次
    batch_counter = 1
    for crop in harvested_crops:
        # 为每个地块创建2-3个采摘批次
        for i in range(random.randint(2, 3)):
            harvest_date = datetime(2026, 1, random.randint(10, 31)).date()
            batch_number = f'KRL-{crop.Cid}-{harvest_date.strftime("%Y%m%d")}-{str(batch_counter).zfill(3)}'
            
            if not Livestock.objects.filter(Tag_number=batch_number).exists():
                Livestock.objects.create(
                    user=admin_user,
                    Tag_number=batch_number,
                    Animal_type=f'香梨采摘批次-{crop.Field_name}',
                    Age=random.randint(1, 3),  # 存续时长（年）
                    Breed=f'库尔勒香梨-{crop.Variety}'
                )
                batch_counter += 1
                print(f"   ✓ 创建采摘批次: {batch_number} (来自: {crop.Field_name})")
    
    print(f"   总计: {Livestock.objects.filter(user=admin_user).count()} 个采摘批次")
    
    # 5. 创建农机设备数据
    print("\n5. 创建农机设备数据...")
    machinery_data = [
        {'Number_plate': 'JD8500-KRL-001', 'Equipment_name': '约翰迪尔收割机', 
         'Purchase_price': 850000.00, 'Purchase_date': '2022-05-10', 
         'Operation': '用于香梨收获作业，效率高，操作简便'},
        {'Number_plate': 'DFH804-KRL-002', 'Equipment_name': '东方红拖拉机', 
         'Purchase_price': 450000.00, 'Purchase_date': '2022-06-15', 
         'Operation': '用于耕地、运输，多功能农用机械'},
        {'Number_plate': 'SPR350-KRL-003', 'Equipment_name': '喷雾机', 
         'Purchase_price': 120000.00, 'Purchase_date': '2023-03-20', 
         'Operation': '用于农药喷洒，精准施药'},
        {'Number_plate': 'TRK150-KRL-004', 'Equipment_name': '运输车', 
         'Purchase_price': 180000.00, 'Purchase_date': '2023-07-10', 
         'Operation': '用于香梨运输，载重量大'},
    ]
    
    machinery_created = 0
    for machine in machinery_data:
        if not Machinery.objects.filter(Number_plate=machine['Number_plate']).exists():
            Machinery.objects.create(user=admin_user, **machine)
            machinery_created += 1
            print(f"   ✓ 创建农机设备: {machine['Equipment_name']}")
    
    print(f"   总计: {Machinery.objects.filter(user=admin_user).count()} 台农机设备")
    
    # 6. 创建产量分析数据（2026年1月-2月）
    print("\n6. 创建产量分析数据（2026年1月-2月）...")
    
    # 生成2026年1月和2月的生产数据
    months = [(2026, 1), (2026, 2)]
    milk_production_created = 0
    egg_production_created = 0
    
    for year, month in months:
        # 确定该月的天数
        if month == 2:
            days_in_month = 28  # 2026年不是闰年
        else:
            days_in_month = 31
        
        for day in range(1, days_in_month + 1):
            # 创建Milk_production数据（产量分析）
            if not Milk_production.objects.filter(Year=year, Month=month, Day=day).exists():
                Milk_production.objects.create(
                    user=admin_user,
                    Year=year,
                    Month=month,
                    Day=day,
                    Livestock_number=random.randint(50, 100),  # 作业规模
                    Morning_production=random.randint(200, 500),  # 上午产量
                    Midday_production=random.randint(300, 600),  # 中午产量
                    Evening_production=random.randint(250, 550),  # 晚上产量
                    Morning_consumption=random.randint(100, 300),  # 上午消耗
                    Evening_consumption=random.randint(100, 300),  # 晚上消耗
                )
                milk_production_created += 1
            
            # 创建Eggs_production数据（质量分析）
            if not Eggs_production.objects.filter(Year=year, Month=month, Day=day).exists():
                Eggs_production.objects.create(
                    user=admin_user,
                    Year=year,
                    Month=month,
                    Day=day,
                    Poultry_number=f"地块{random.choice([2001, 2002])}",  # 地块编号
                    Morning_egg_collection=random.randint(100, 400),  # 上午采摘量
                    Midday_egg_collection=random.randint(150, 450),  # 中午采摘量
                    Evening_egg_collection=random.randint(120, 420),  # 下午采摘量
                    Morning_feeds=random.randint(50, 200),  # 农资消耗(上午)
                    Evening_feeds=random.randint(50, 200),  # 农资消耗(下午)
                    Comments=f'{year}年{month}月{day}日生产记录，天气良好，采摘顺利'
                )
                egg_production_created += 1
    
    print(f"   产量分析记录: {milk_production_created} 条")
    print(f"   质量分析记录: {egg_production_created} 条")
    
    # 7. 打印统计信息
    print("\n" + "=" * 70)
    print("数据生成完成！统计信息：")
    print("=" * 70)
    print(f"Currently there are {Employees.objects.filter(user=admin_user).count()} employees in the database.")
    print(f"Currently there are {Crops.objects.filter(user=admin_user).count()} crops in the database.")
    print(f"Currently there are {Livestock.objects.filter(user=admin_user).count()} livestock batches in the database.")
    print(f"Currently there are {Machinery.objects.filter(user=admin_user).count()} machinery items in the database.")
    print(f"Currently there are {Milk_production.objects.filter(user=admin_user).count()} milk production records in the database.")
    print(f"Currently there are {Eggs_production.objects.filter(user=admin_user).count()} egg production records in the database.")
    
    print("\n" + "=" * 70)
    print("✅ 演示数据生成完成！")
    print("=" * 70)
    print("\n系统访问信息:")
    print("  • 访问地址: http://127.0.0.1:8080")
    print("  • 管理员账号: admin / 123456")
    print("\n主要功能模块数据统计:")
    print("  1. 员工管理: 5名员工")
    print("  2. 种植档案管理: 3个地块")
    print("  3. 采摘批次管理: 多个批次（与地块关联）")
    print("  4. 农机设备管理: 4台设备")
    print("  5. 产量分析: 2026年1月-2月完整数据")
    print("  6. 质量分析: 2026年1月-2月完整数据")
    print("\n现在您可以:")
    print("  1. 访问 http://127.0.0.1:8080 查看系统")
    print("  2. 使用 admin/123456 登录")
    print("  3. 查看所有页面中的数据展示")

if __name__ == '__main__':
    create_seed_data()