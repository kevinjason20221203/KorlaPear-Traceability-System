#!/usr/bin/env python
"""
添加测试产量数据脚本
用于测试产量分析图表功能
"""

import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KorlaPearTraceabilitySystem.settings')
django.setup()

from homepage.models import Milk_production
from django.contrib.auth.models import User

def add_test_data():
    """添加测试产量数据"""
    
    # 获取或创建测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    
    # 删除现有测试数据（2026年3月）
    Milk_production.objects.filter(Year=2026, Month=3, user=user).delete()
    
    # 添加测试数据 - 2026年3月1-10日
    test_data = [
        # Day, Livestock_number, Morning_production, Midday_production, Evening_production, Morning_consumption, Evening_consumption
        (1, 50, 120.5, 80.3, 95.2, 45.2, 30.1),
        (2, 52, 125.3, 85.1, 98.7, 48.3, 32.5),
        (3, 55, 130.8, 90.5, 102.3, 50.1, 35.2),
        (4, 53, 128.6, 88.7, 100.5, 49.2, 33.8),
        (5, 58, 140.2, 95.8, 110.3, 55.3, 38.7),
        (6, 60, 145.6, 98.9, 115.2, 58.1, 40.2),
        (7, 62, 150.3, 102.5, 120.8, 60.5, 42.3),
        (8, 61, 148.7, 100.9, 118.6, 59.8, 41.5),
        (9, 65, 155.2, 105.8, 125.3, 62.7, 44.1),
        (10, 68, 160.8, 110.3, 130.5, 65.2, 46.3),
    ]
    
    records_added = 0
    for day, livestock_num, morning_prod, midday_prod, evening_prod, morning_cons, evening_cons in test_data:
        record = Milk_production.objects.create(
            user=user,
            Year=2026,
            Month=3,
            Day=day,
            Livestock_number=livestock_num,
            Morning_production=morning_prod,
            Midday_production=midday_prod,
            Evening_production=evening_prod,
            Morning_consumption=morning_cons,
            Evening_consumption=evening_cons
        )
        records_added += 1
        print(f"✅ 添加记录: 2026年3月{day}日 - 总产量: {record.Total_production:.1f}kg, 总消耗: {record.Total_consumption:.1f}kg")
    
    print(f"\n🎉 成功添加 {records_added} 条测试产量记录")
    print("📊 现在可以访问 http://127.0.0.1:8080/select_yearmonth/ 选择2026年3月查看图表")

def check_existing_data():
    """检查现有数据"""
    print("📋 检查现有产量数据...")
    
    # 检查所有年份月份的数据
    all_data = Milk_production.objects.all().order_by('Year', 'Month', 'Day')
    
    if all_data:
        print(f"现有数据记录数: {all_data.count()}")
        
        # 按年月分组统计
        from collections import defaultdict
        year_month_stats = defaultdict(int)
        
        for record in all_data:
            key = f"{record.Year}年{record.Month}月"
            year_month_stats[key] += 1
        
        print("按年月统计:")
        for ym, count in year_month_stats.items():
            print(f"  {ym}: {count}条记录")
    else:
        print("⚠️ 数据库中没有产量记录")

if __name__ == "__main__":
    print("=" * 50)
    print("库尔勒香梨产量分析 - 测试数据生成脚本")
    print("=" * 50)
    
    # 检查现有数据
    check_existing_data()
    
    print("\n" + "=" * 50)
    print("开始添加测试数据...")
    print("=" * 50)
    
    # 添加测试数据
    add_test_data()
    
    print("\n" + "=" * 50)
    print("脚本执行完成！")
    print("=" * 50)