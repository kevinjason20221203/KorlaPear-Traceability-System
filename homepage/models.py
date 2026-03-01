from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MaxValueValidator,MinValueValidator
import qrcode
from io import BytesIO
from django.core.files import File
import uuid
from django.utils import timezone

# Create your models here.


class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    Eid = models.IntegerField(primary_key=True, default=0, verbose_name="员工ID")
    Name = models.CharField(max_length=50, verbose_name="姓名")
    Country_code = models.CharField(max_length=4, verbose_name="国家代码")
    Phone_number = models.CharField(max_length=9, verbose_name="电话号码")
    Position = models.CharField(max_length=10, verbose_name="职位")
    Salary = models.IntegerField(verbose_name="薪资")
    Performance = models.CharField(max_length=10, verbose_name="绩效")

    class Meta:
        db_table = "employees"
        verbose_name = "员工信息"
        verbose_name_plural = "员工信息"


class Crops(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    Cid = models.IntegerField(primary_key=True, default=0, verbose_name="地块ID")
    Field_name = models.CharField(max_length=50, verbose_name="地块名称")
    Field_description = models.TextField(verbose_name="地块描述")
    Crop_name = models.CharField(max_length=50, verbose_name="品种")
    Variety = models.CharField(max_length=20, verbose_name="品种类型")
    Planting_date = models.DateField(verbose_name="种植日期")
    Is_harvested = models.BooleanField(default=False, verbose_name="是否已采摘")
    Harvesting_date = models.DateField(null=True, blank=True, verbose_name="采摘日期")

    def calculate_profit(self):
        if self.Harvesting_date and self.Sales:
            expenses_total = self.Expenses
            return self.Sales - expenses_total
        else:
            return None
    
    class Meta:
        verbose_name = "香梨种植地块"
        verbose_name_plural = "香梨种植地块"
        
class Crop_expenses(models.Model):
    crops=models.ForeignKey(Crops,on_delete=models.CASCADE)

    Expense_date=models.DateField(help_text='m/d/y', verbose_name="费用日期")
    Expense_type=models.CharField(max_length=20, verbose_name="费用类型")
    Expense_description=models.TextField(verbose_name="费用描述")
    Budget= models.DecimalField(max_digits=10,decimal_places=2,default=0, verbose_name="预算")
    Expense_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0, verbose_name="费用金额")
    Supplier=models.CharField(max_length=20, verbose_name="供应商")
    Payment_method=models.CharField(max_length=10, verbose_name="支付方式")
    Receipt_number=models.CharField(max_length=20, verbose_name="收据编号")

    class Meta:
        db_table="Crop_expenses"
        verbose_name = "种植费用"
        verbose_name_plural = "种植费用"


class Crop_sales(models.Model):
    crops=models.ForeignKey(Crops,on_delete=models.CASCADE)

    Sale_date=models.DateField(help_text='m/d/y', verbose_name="销售日期")
    Quantity_sold=models.CharField(max_length=20, verbose_name="销售数量")
    Unit_price=models.DecimalField(max_digits=10,decimal_places=2,default=0, verbose_name="单价")
    Total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False, verbose_name="总价")
    Buyer_information=models.TextField(verbose_name="买家信息")
    Payment_method=models.CharField(max_length=20, verbose_name="支付方式")
    Payment_status=models.CharField(max_length=20, choices=[('pending', '待支付'), ('received', '已支付')], verbose_name="支付状态")
    Invoice_number=models.CharField(max_length=20, verbose_name="发票编号")
    Additional_notes=models.TextField(blank=True, verbose_name="备注")


#lets over ride the save method in order before saving it calculates the total amount


    def save(self, *args, **kwargs):
        # Convert Decimal values to float for multiplication
        quantity_sold = float(self.Quantity_sold)
        unit_price = float(self.Unit_price)

            # Calculate total sale amount before saving
        self.Total_price = Decimal(quantity_sold * unit_price)
        super().save(*args, **kwargs) #here we are calling the initial save 
    
    class Meta:
        verbose_name = "采摘批次管理"
        verbose_name_plural = "采摘批次管理"

class Crop_operations(models.Model):
    crops=models.ForeignKey(Crops,on_delete=models.CASCADE)

    Operation_date=models.DateField(help_text="m/d/y", verbose_name="操作日期")
    Operation_name=models.CharField(max_length=20, verbose_name="操作名称")
    Additional_notes=models.TextField(blank=True, verbose_name="备注")

    class Meta:
        db_table="Crop_operations"
        verbose_name = "种植操作"
        verbose_name_plural = "种植操作"

    

        
class Machinery(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    
    Number_plate= models.CharField(max_length=20, primary_key=True, verbose_name="设备编号")
    Equipment_name= models.CharField(max_length=20, verbose_name="设备名称")
    Purchase_price= models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name="购买价格")
    Purchase_date = models.DateField(verbose_name="购买日期")
    Operation=models.TextField(blank=True, verbose_name="操作说明")

    class Meta:
        db_table = "Machinery"
        verbose_name = "机械设备"
        verbose_name_plural = "机械设备"

class Machinery_activities(models.Model):
    machinery= models.ForeignKey(Machinery,on_delete=models.CASCADE)

    Activity_date=models.DateField(help_text="m/d/y")
    Activity_type=models.CharField(max_length=20)
    Activity_cost=models.IntegerField(blank=True)
    Description=models.TextField(blank=True)

    class meta:
        db_table="Machinery_activities"

class Machinery_maintenance(models.Model):
    machinery=models.ForeignKey(Machinery,on_delete=models.CASCADE)

    Date= models.DateField(help_text="m/d/y")
    Machinery_part=models.CharField(max_length=100)
    Technician_details=models.CharField(max_length=100,blank="True")
    Cost= models.IntegerField()
    Description=models.TextField()

    class Meta:
        db_table="Machinery_activities"


class Livestock(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    Tag_number = models.CharField(max_length=20, primary_key=True, verbose_name="追踪编号")
    Animal_type= models.CharField(max_length=20, verbose_name="物流类型")
    Age= models.IntegerField(verbose_name="存储时长(天)")
    Breed= models.CharField(max_length=20, verbose_name="产品规格")

    class Meta:
        db_table = "Livestock"
        verbose_name = "物流追踪记录"
        verbose_name_plural = "物流追踪记录"

    

class Livestock_production(models.Model):
    livestock=models.ForeignKey(Livestock,on_delete=models.CASCADE)
    Production_date=models.DateField(help_text='m/d/y', verbose_name="生产日期")
    Production_amount=models.CharField(max_length=20, verbose_name="生产数量")
    Feed_consumed=models.DecimalField(max_digits=10,decimal_places=2,help_text='field consumed in kg', verbose_name="饲料消耗")
    Comments=models.TextField(null=True,blank=True, verbose_name="备注")

    class Meta:
        db_table="Livestock_production"
        verbose_name = "物流生产记录"
        verbose_name_plural = "物流生产记录"

class Milk_production(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1)


    Year=models.IntegerField(validators=[MinValueValidator(1)], verbose_name="年份")
    Month=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name="月份")
    Day=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)],default=1, verbose_name="日期")

    Livestock_number=models.IntegerField(verbose_name="牲畜数量")
    Morning_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres', verbose_name="早晨产量")
    Midday_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres', blank=True, verbose_name="中午产量")
    Evening_production=models.DecimalField(max_digits=10,decimal_places=2,help_text='production in litres',blank=True, verbose_name="晚上产量")
    Total_production=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False, verbose_name="总产量")

    Morning_consumption=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg', verbose_name="早晨消耗")
    Evening_consumption=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg',blank=True, verbose_name="晚上消耗")
    Total_consumption=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False, verbose_name="总消耗")

    def save(self,*args,**kwargs):
        morning_production=float(self.Morning_production)
        midday_production=float(self.Midday_production)
        evening_production=float(self.Evening_production)

        self.Total_production=Decimal(morning_production+midday_production+evening_production)

        morning_consumption=float(self.Morning_consumption)
        evening_consumption=float(self.Evening_consumption)

        self.Total_consumption=Decimal(morning_consumption+evening_consumption)

        super().save(*args,**kwargs)
    
    class Meta:
        verbose_name = "产量记录"
        verbose_name_plural = "产量记录"


class Eggs_production(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=1)

    Year =models.IntegerField(validators=[MinValueValidator(1)], verbose_name="年份")
    Month = models.IntegerField(validators= [MinValueValidator(1), MaxValueValidator(12)], verbose_name="月份")
    Day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)], verbose_name="日期")
    Poultry_number=models.IntegerField(verbose_name="家禽数量")

    Morning_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected', verbose_name="早晨收集")
    Midday_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected', blank=True, verbose_name="中午收集")
    Evening_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,help_text='total number of eggs collected',blank=True, verbose_name="晚上收集")
    Total_egg_collection=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False, verbose_name="总收集")

    Morning_feeds=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg', verbose_name="早晨饲料")
    Evening_feeds=models.DecimalField(max_digits=10,decimal_places=2,help_text='feed consumed in kg',blank=True, verbose_name="晚上饲料")
    Total_feeds=models.DecimalField(max_digits=10,decimal_places=2,default=0,editable=False, verbose_name="总饲料")
    Comments=models.TextField(null=True,blank=True, verbose_name="备注")

    def save(self,*args, **kwargs):
        morning_egg_collection=float(self.Morning_egg_collection)
        midday_egg_collection=float(self.Midday_egg_collection)
        evening_egg_collection=float(self.Evening_egg_collection)

        self.Total_egg_collection=Decimal(morning_egg_collection+midday_egg_collection+evening_egg_collection)

        morning_feeds=float(self.Morning_feeds)
        evening_feeds=float(self.Evening_feeds)

        self.Total_feeds=Decimal(morning_feeds+evening_feeds)
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "禽蛋记录"
        verbose_name_plural = "禽蛋记录"


# ==================== 二维码批次管理模块 ====================

class QRCodeBatch(models.Model):
    """二维码批次管理 - 关联采摘批次生成唯一二维码"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="用户")
    
    # 外键关联采摘批次（Livestock模型）
    livestock = models.ForeignKey('Livestock', on_delete=models.CASCADE, verbose_name="关联采摘批次")
    
    # 二维码唯一序列号（格式：KRL-QR-YYYYMMDD-XXXX）
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="二维码序列号")
    
    # 二维码图片存储
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name="二维码图片")
    
    # 二维码内容（包含溯源信息的URL）
    qr_content = models.TextField(verbose_name="二维码内容")
    
    # 状态管理
    STATUS_CHOICES = [
        ('generated', '已生成'),
        ('printed', '已打印'),
        ('attached', '已贴标'),
        ('scanned', '已扫描'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generated', verbose_name="状态")
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_scanned = models.DateTimeField(null=True, blank=True, verbose_name="最后扫描时间")
    
    def generate_qr_code(self):
        """生成二维码图片"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.qr_content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 保存到内存
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        # 保存到ImageField
        filename = f'qrcode_{self.serial_number}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()
    
    def save(self, *args, **kwargs):
        """重写save方法，自动生成二维码"""
        if not self.serial_number:
            # 生成唯一序列号：KRL-QR-YYYYMMDD-UUID前8位
            date_str = timezone.now().strftime('%Y%m%d')
            uuid_str = str(uuid.uuid4())[:8]
            self.serial_number = f"KRL-QR-{date_str}-{uuid_str}"
        
        if not self.qr_content:
            # 生成包含溯源信息的URL
            self.qr_content = f"http://127.0.0.1:8080/trace/{self.serial_number}/"
        
        # 生成二维码图片
        self.generate_qr_code()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.serial_number} - {self.livestock.Tag_number}"
    
    class Meta:
        verbose_name = "二维码批次管理"
        verbose_name_plural = "二维码批次管理"
        ordering = ['-created_at']


class QRCodeScanLog(models.Model):
    """二维码扫描日志记录"""
    qr_code = models.ForeignKey(QRCodeBatch, on_delete=models.CASCADE, verbose_name="二维码")
    scanned_at = models.DateTimeField(auto_now_add=True, verbose_name="扫描时间")
    scanner_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="扫描IP")
    scanner_location = models.CharField(max_length=100, blank=True, verbose_name="扫描地点")
    scan_type = models.CharField(max_length=20, choices=[
        ('production', '生产环节'),
        ('storage', '仓储环节'),
        ('logistics', '物流环节'),
        ('retail', '零售环节'),
        ('consumer', '消费者查询'),
    ], verbose_name="扫描类型")
    
    def __str__(self):
        return f"{self.qr_code.serial_number} - {self.scanned_at}"
    
    class Meta:
        verbose_name = "二维码扫描日志"
        verbose_name_plural = "二维码扫描日志"
        ordering = ['-scanned_at']


# ==================== 物流追踪系统模块 ====================

class LogisticsTracking(models.Model):
    """物流追踪记录 - 记录采摘批次从采摘到销售的完整物流过程"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="操作员")
    
    # 外键关联采摘批次
    livestock = models.ForeignKey('Livestock', on_delete=models.CASCADE, verbose_name="关联采摘批次")
    
    # 物流状态
    STATUS_CHOICES = [
        ('picked', '已采摘'),
        ('sorted', '已分拣'),
        ('packaged', '已包装'),
        ('stored', '已入库'),
        ('inspected', '已质检'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('sold', '已销售'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="物流状态")
    
    # 位置信息
    location = models.CharField(max_length=100, verbose_name="当前位置")
    location_type = models.CharField(max_length=20, choices=[
        ('farm', '果园'),
        ('packing_house', '包装厂'),
        ('cold_storage', '冷库'),
        ('distribution_center', '配送中心'),
        ('retail_store', '零售店'),
        ('customer', '消费者'),
    ], verbose_name="位置类型")
    
    # 环境参数（用于冷链物流）
    temperature = models.FloatField(null=True, blank=True, verbose_name="温度(℃)")
    humidity = models.FloatField(null=True, blank=True, verbose_name="湿度(%)")
    
    # 操作信息
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='logistics_operations', verbose_name="操作人员")
    operation_notes = models.TextField(blank=True, verbose_name="操作备注")
    
    # 时间戳
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")
    expected_next_time = models.DateTimeField(null=True, blank=True, verbose_name="预计下一环节时间")
    
    def __str__(self):
        return f"{self.livestock.Tag_number} - {self.get_status_display()} - {self.timestamp}"
    
    class Meta:
        verbose_name = "物流追踪记录"
        verbose_name_plural = "物流追踪记录"
        ordering = ['-timestamp']


class Storage(models.Model):
    """仓储管理 - 存储采摘批次的环境信息"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="负责人")
    
    storage_name = models.CharField(max_length=100, verbose_name="仓库名称")
    storage_type = models.CharField(max_length=20, choices=[
        ('cold_storage', '冷库'),
        ('normal_storage', '普通仓库'),
        ('packing_area', '包装区'),
        ('temporary', '临时存放区'),
    ], verbose_name="仓库类型")
    
    # 仓储容量信息
    capacity = models.FloatField(verbose_name="容量(吨)")
    current_usage = models.FloatField(default=0, verbose_name="当前使用量(吨)")
    
    # 位置信息
    address = models.TextField(verbose_name="仓库地址")
    latitude = models.FloatField(null=True, blank=True, verbose_name="纬度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="经度")
    
    # 环境参数
    optimal_temperature = models.FloatField(null=True, blank=True, verbose_name="最佳温度(℃)")
    optimal_humidity = models.FloatField(null=True, blank=True, verbose_name="最佳湿度(%)")
    
    # 管理信息
    manager_name = models.CharField(max_length=50, verbose_name="仓库管理员")
    contact_phone = models.CharField(max_length=20, verbose_name="联系电话")
    
    # 状态
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return f"{self.storage_name} ({self.get_storage_type_display()})"
    
    def get_usage_percentage(self):
        """获取仓库使用率"""
        if self.capacity > 0:
            return round((self.current_usage / self.capacity) * 100, 2)
        return 0
    
    class Meta:
        verbose_name = "仓储管理"
        verbose_name_plural = "仓储管理"
        ordering = ['storage_name']


class StorageItem(models.Model):
    """仓储物品 - 记录具体批次在仓库中的存储情况"""
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="所属仓库")
    livestock = models.ForeignKey('Livestock', on_delete=models.CASCADE, verbose_name="关联采摘批次")
    
    # 存储信息
    date_stored = models.DateTimeField(auto_now_add=True, verbose_name="入库时间")
    date_removed = models.DateTimeField(null=True, blank=True, verbose_name="出库时间")
    storage_duration = models.IntegerField(null=True, blank=True, verbose_name="存储时长(小时)")
    
    # 数量信息
    quantity = models.FloatField(verbose_name="数量(公斤)")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价(元/公斤)")
    total_value = models.DecimalField(max_digits=12, decimal_places=2, editable=False, verbose_name="总价值(元)")
    
    # 质量信息
    quality_grade = models.CharField(max_length=10, choices=[
        ('premium', '特级'),
        ('grade_a', '一级'),
        ('grade_b', '二级'),
        ('grade_c', '三级'),
    ], verbose_name="质量等级")
    
    # 环境记录
    storage_temperature = models.FloatField(null=True, blank=True, verbose_name="存储温度(℃)")
    storage_humidity = models.FloatField(null=True, blank=True, verbose_name="存储湿度(%)")
    
    # 状态
    is_in_storage = models.BooleanField(default=True, verbose_name="是否在库")
    notes = models.TextField(blank=True, verbose_name="备注")
    
    def save(self, *args, **kwargs):
        """重写save方法，自动计算总价值和存储时长"""
        # 计算总价值
        if self.quantity and self.unit_price:
            self.total_value = self.quantity * self.unit_price
        
        # 计算存储时长（如果已出库）
        if self.date_removed and self.date_stored:
            duration = self.date_removed - self.date_stored
            self.storage_duration = duration.total_seconds() / 3600  # 转换为小时
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.livestock.Tag_number} - {self.storage.storage_name}"
    
    class Meta:
        verbose_name = "仓储物品"
        verbose_name_plural = "仓储物品"
        ordering = ['-date_stored']





