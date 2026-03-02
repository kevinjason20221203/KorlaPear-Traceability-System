#!/usr/bin/env python
"""
为库尔勒香梨生产溯源管理系统添加测试数据
包括：采摘批次、仓储管理、物流追踪、二维码管理等联动数据
"""

import os
import sys
import django
from django.utils import timezone
from datetime import datetime, timedelta
import random

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KorlaPearTraceabilitySystem.settings')
django.setup()

from django.contrib.auth.models import User
from homepage.models import (
    Livestock, Storage, LogisticsTracking, QRCodeBatch, 
    StorageItem, QRCodeScanLog
)

def create_test_user():
    """创建测试用户"""
    try:
        user = User.objects.get(username='admin')
        print(f"使用现有用户: {user.username}")
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='admin',
            password='123456',
            email='admin@kuerle-pear.com',
            is_staff=True,
            is_superuser=True
        )
        print(f"创建新用户: {user.username}")
        return user

def create_livestock_batches(user):
    """创建采摘批次测试数据"""
    print("\n=== 创建采摘批次测试数据 ===")
    
    livestock_data = [
        {
            'Tag_number': 'KRL-2024-001',
            'Animal_type': '特级香梨',
            'Age': 15,
            'Breed': '库尔勒香梨-A级'
        },
        {
            'Tag_number': 'KRL-2024-002',
            'Animal_type': '一级香梨',
            'Age': 12,
            'Breed': '库尔勒香梨-B级'
        },
        {
            'Tag_number': 'KRL-2024-003',
            'Animal_type': '特级香梨',
            'Age': 18,
            'Breed': '库尔勒香梨-A级'
        },
        {
            'Tag_number': 'KRL-2024-004',
            'Animal_type': '二级香梨',
            'Age': 10,
            'Breed': '库尔勒香梨-C级'
        },
        {
            'Tag_number': 'KRL-2024-005',
            'Animal_type': '一级香梨',
            'Age': 14,
            'Breed': '库尔勒香梨-B级'
        }
    ]
    
    created_batches = []
    for data in livestock_data:
        try:
            livestock = Livestock.objects.get(Tag_number=data['Tag_number'])
            print(f"批次已存在: {livestock.Tag_number}")
            created_batches.append(livestock)
        except Livestock.DoesNotExist:
            livestock = Livestock.objects.create(
                user=user,
                Tag_number=data['Tag_number'],
                Animal_type=data['Animal_type'],
                Age=data['Age'],
                Breed=data['Breed']
            )
            print(f"创建采摘批次: {livestock.Tag_number} - {livestock.Animal_type}")
            created_batches.append(livestock)
    
    return created_batches

def create_storage_facilities(user):
    """创建仓储设施测试数据"""
    print("\n=== 创建仓储设施测试数据 ===")
    
    storage_data = [
        {
            'storage_name': '库尔勒中心冷库',
            'storage_type': 'cold_storage',
            'capacity': 500.0,
            'current_usage': 320.5,
            'address': '新疆库尔勒市香梨大道1号',
            'optimal_temperature': 2.0,
            'optimal_humidity': 85.0,
            'manager_name': '张经理',
            'contact_phone': '13800138001'
        },
        {
            'storage_name': '包装加工中心',
            'storage_type': 'packing_area',
            'capacity': 200.0,
            'current_usage': 150.0,
            'address': '新疆库尔勒市果园路88号',
            'optimal_temperature': 18.0,
            'optimal_humidity': 60.0,
            'manager_name': '李主任',
            'contact_phone': '13800138002'
        },
        {
            'storage_name': '临时存放区',
            'storage_type': 'temporary',
            'capacity': 100.0,
            'current_usage': 45.0,
            'address': '新疆库尔勒市采摘基地内',
            'optimal_temperature': 25.0,
            'optimal_humidity': 65.0,
            'manager_name': '王管理员',
            'contact_phone': '13800138003'
        }
    ]
    
    created_storages = []
    for data in storage_data:
        try:
            storage = Storage.objects.get(storage_name=data['storage_name'])
            print(f"仓库已存在: {storage.storage_name}")
            created_storages.append(storage)
        except Storage.DoesNotExist:
            storage = Storage.objects.create(
                user=user,
                **data
            )
            print(f"创建仓库: {storage.storage_name} - 容量: {storage.capacity}吨")
            created_storages.append(storage)
    
    return created_storages

def create_logistics_tracking(user, livestock_batches):
    """创建物流追踪测试数据"""
    print("\n=== 创建物流追踪测试数据 ===")
    
    # 物流状态序列
    status_sequence = [
        ('picked', '已采摘'),
        ('sorted', '已分拣'),
        ('packaged', '已包装'),
        ('stored', '已入库'),
        ('inspected', '已质检'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('sold', '已销售')
    ]
    
    # 位置信息
    locations = {
        'picked': '库尔勒香梨果园3号地块',
        'sorted': '包装加工中心分拣区',
        'packaged': '包装加工中心包装区',
        'stored': '库尔勒中心冷库A区',
        'inspected': '质量检测中心',
        'shipped': '库尔勒物流中心',
        'delivered': '北京新发地批发市场',
        'sold': '北京华联超市'
    }
    
    location_types = {
        'picked': 'farm',
        'sorted': 'packing_house',
        'packaged': 'packing_house',
        'stored': 'cold_storage',
        'inspected': 'distribution_center',
        'shipped': 'distribution_center',
        'delivered': 'retail_store',
        'sold': 'customer'
    }
    
    created_tracking = []
    
    for livestock in livestock_batches:
        # 为每个批次创建完整的物流追踪记录
        start_time = timezone.now() - timedelta(days=random.randint(5, 15))
        
        for i, (status_code, status_display) in enumerate(status_sequence[:random.randint(3, 8)]):
            tracking_time = start_time + timedelta(hours=i*random.randint(6, 24))
            
            # 创建物流追踪记录
            tracking = LogisticsTracking.objects.create(
                user=user,
                livestock=livestock,
                status=status_code,
                location=locations[status_code],
                location_type=location_types[status_code],
                temperature=random.uniform(0, 5) if status_code in ['stored', 'shipped'] else None,
                humidity=random.uniform(80, 90) if status_code in ['stored', 'shipped'] else None,
                operator=user,
                operation_notes=f"{livestock.Tag_number}的{status_display}操作记录",
                timestamp=tracking_time
            )
            
            created_tracking.append(tracking)
            print(f"创建物流追踪: {livestock.Tag_number} - {status_display} - {tracking_time.strftime('%Y-%m-%d %H:%M')}")
    
    return created_tracking

def create_qrcode_batches(user, livestock_batches):
    """创建二维码批次测试数据"""
    print("\n=== 创建二维码批次测试数据 ===")
    
    created_qrcodes = []
    
    for livestock in livestock_batches:
        try:
            qrcode = QRCodeBatch.objects.get(livestock=livestock)
            print(f"二维码已存在: {qrcode.serial_number} - {livestock.Tag_number}")
            created_qrcodes.append(qrcode)
        except QRCodeBatch.DoesNotExist:
            qrcode = QRCodeBatch.objects.create(
                user=user,
                livestock=livestock,
                status=random.choice(['generated', 'printed', 'attached', 'scanned'])
            )
            print(f"创建二维码: {qrcode.serial_number} - {livestock.Tag_number} - 状态: {qrcode.get_status_display()}")
            created_qrcodes.append(qrcode)
            
            # 为部分二维码创建扫描记录
            if qrcode.status == 'scanned':
                for _ in range(random.randint(1, 3)):
                    scan_time = timezone.now() - timedelta(days=random.randint(1, 7))
                    QRCodeScanLog.objects.create(
                        qr_code=qrcode,
                        scanned_at=scan_time,
                        scanner_ip=f"192.168.1.{random.randint(1, 255)}",
                        scanner_location=random.choice(['果园', '包装厂', '冷库', '超市']),
                        scan_type=random.choice(['production', 'storage', 'logistics', 'retail', 'consumer'])
                    )
                print(f"  添加了扫描记录")
    
    return created_qrcodes

def create_storage_items(user, livestock_batches, storage_facilities):
    """创建仓储物品测试数据"""
    print("\n=== 创建仓储物品测试数据 ===")
    
    created_items = []
    
    for livestock in livestock_batches[:3]:  # 只为前3个批次创建仓储记录
        storage = random.choice(storage_facilities)
        
        try:
            item = StorageItem.objects.get(livestock=livestock, storage=storage)
            print(f"仓储物品已存在: {livestock.Tag_number} - {storage.storage_name}")
            created_items.append(item)
        except StorageItem.DoesNotExist:
            # 随机决定是否已出库
            is_in_storage = random.choice([True, False])
            date_stored = timezone.now() - timedelta(days=random.randint(1, 10))
            date_removed = None if is_in_storage else date_stored + timedelta(days=random.randint(1, 5))
            
            item = StorageItem.objects.create(
                storage=storage,
                livestock=livestock,
                date_stored=date_stored,
                date_removed=date_removed,
                quantity=random.uniform(100, 500),
                unit_price=random.uniform(8.0, 15.0),
                quality_grade=random.choice(['premium', 'grade_a', 'grade_b', 'grade_c']),
                storage_temperature=random.uniform(0, 5) if storage.storage_type == 'cold_storage' else random.uniform(15, 25),
                storage_humidity=random.uniform(80, 90) if storage.storage_type == 'cold_storage' else random.uniform(50, 70),
                is_in_storage=is_in_storage,
                notes=f"{livestock.Animal_type}批次存储记录"
            )
            
            print(f"创建仓储物品: {livestock.Tag_number} - {storage.storage_name} - 数量: {item.quantity:.1f}公斤")
            created_items.append(item)
    
    return created_items

def main():
    """主函数：创建所有测试数据"""
    print("开始为库尔勒香梨生产溯源管理系统创建测试数据...")
    
    try:
        # 1. 创建/获取用户
        user = create_test_user()
        
        # 2. 创建采摘批次
        livestock_batches = create_livestock_batches(user)
        
        # 3. 创建仓储设施
        storage_facilities = create_storage_facilities(user)
        
        # 4. 创建物流追踪
        logistics_tracking = create_logistics_tracking(user, livestock_batches)
        
        # 5. 创建二维码批次
        qrcode_batches = create_qrcode_batches(user, livestock_batches)
        
        # 6. 创建仓储物品
        storage_items = create_storage_items(user, livestock_batches, storage_facilities)
        
        # 7. 打印统计信息
        print("\n" + "="*60)
        print("测试数据创建完成！统计信息：")
        print("="*60)
        print(f"采摘批次数量: {len(livestock_batches)}")
        print(f"仓储设施数量: {len(storage_facilities)}")
        print(f"物流追踪记录: {len(logistics_tracking)}")
        print(f"二维码批次数量: {len(qrcode_batches)}")
        print(f"仓储物品数量: {len(storage_items)}")
        print(f"二维码扫描记录: {QRCodeScanLog.objects.count()}")
        print("="*60)
        print("\n数据联动关系：")
        print("1. 每个采摘批次都有对应的二维码")
        print("2. 每个采摘批次都有完整的物流追踪记录")
        print("3. 部分采摘批次有仓储记录")
        print("4. 部分二维码有扫描记录")
        print("5. 所有数据都关联到同一个用户")
        
    except Exception as e:
        print(f"创建测试数据时出错: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())