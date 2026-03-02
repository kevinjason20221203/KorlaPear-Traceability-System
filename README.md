# 库尔勒香梨生产溯源管理系统

基于Django框架开发的库尔勒香梨全产业链溯源管理系统，实现从种植、采摘、仓储、物流到销售的全流程数字化管理，为消费者提供完整的香梨溯源信息。

![系统首页](static/images/logo.png)

## 目录

- [项目简介](#项目简介)
- [系统功能](#系统功能)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [系统配置](#系统配置)
- [数据管理](#数据管理)
- [部署说明](#部署说明)
- [开发指南](#开发指南)
- [许可证](#许可证)
- [联系我们](#联系我们)

## 项目简介

### 项目背景
库尔勒香梨作为新疆特色农产品，具有极高的品牌价值和市场认可度。为提升产品品质、保障食品安全、增强消费者信任，本项目开发了这套完整的生产溯源管理系统。

### 项目目标
1. **全流程追溯**: 实现从果园到餐桌的完整溯源链条
2. **数字化管理**: 将传统农业生产过程数字化、信息化
3. **品质保障**: 通过环境监控和质量控制确保产品品质
4. **品牌提升**: 通过溯源系统增强品牌价值和消费者信任

### 核心价值
- **消费者**: 扫码即可查看香梨完整生产信息
- **生产者**: 数字化管理提升生产效率和质量控制
- **监管者**: 实时监控生产过程，保障食品安全
- **经销商**: 完整的物流信息，提升供应链透明度

## 系统功能

### 1. 种植管理模块 🌱
- **地块管理**: 记录香梨种植地块信息、品种、种植日期
- **种植操作**: 记录施肥、灌溉、修剪等农事操作
- **费用管理**: 记录种植过程中的各项费用支出
- **销售管理**: 记录香梨销售信息，包括价格、数量、买家

### 2. 采摘批次管理 🍐
- **批次追踪**: 为每个采摘批次生成唯一追踪编号
- **质量分级**: 根据香梨品质进行分级管理
- **采摘记录**: 记录采摘时间、地点、负责人等信息
- **批次关联**: 将采摘批次与种植地块、二维码关联

### 3. 二维码溯源管理 📱
- **二维码生成**: 为每个采摘批次生成唯一二维码
- **扫码查询**: 消费者扫码即可查看完整溯源信息
- **状态管理**: 二维码生成、打印、贴标、扫描全流程管理
- **扫描记录**: 记录二维码的扫描时间、地点、类型

### 4. 物流追踪管理 🚚
- **物流状态**: 实时追踪香梨从采摘到销售的物流状态
- **环境监控**: 记录运输和存储过程中的温度、湿度
- **位置跟踪**: 记录香梨在物流链中的当前位置
- **时间线展示**: 可视化展示香梨的完整物流时间线

### 5. 仓储管理模块 📦
- **仓库管理**: 管理冷库、普通仓库、包装区等存储设施
- **库存管理**: 实时监控仓库库存和使用率
- **入库出库**: 完整的入库和出库操作流程
- **环境监控**: 监控仓库的温度、湿度等环境参数

### 6. 系统管理模块 ⚙️
- **用户管理**: 管理员、操作员、消费者等多角色权限管理
- **数据统计**: 生产数据、销售数据、物流数据的统计分析
- **系统设置**: 系统参数配置和个性化设置
- **帮助文档**: 完整的系统使用说明和操作指南

## 技术架构

### 后端技术栈
- **框架**: Django 5.0
- **数据库**: SQLite3 (开发) / PostgreSQL (生产)
- **模板引擎**: Django Templates
- **认证系统**: Django Authentication
- **文件存储**: Django Media Files

### 前端技术栈
- **HTML/CSS**: 响应式布局，适配各种设备
- **JavaScript**: 交互功能实现
- **图标库**: Boxicons
- **字体**: Google Fonts (Poppins)

### 第三方库
- **二维码生成**: qrcode, qrcode[pil]
- **图像处理**: Pillow
- **数据可视化**: Matplotlib (统计图表)

### 系统架构
```
┌─────────────────────────────────────────────┐
│                前端界面                      │
│  (HTML/CSS/JavaScript + Django Templates)   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│                Django框架                    │
│  (URL路由 + 视图函数 + 模板渲染 + 表单验证)   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│                数据模型                      │
│  (ORM映射 + 业务逻辑 + 数据验证)              │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│                数据库                        │
│          (SQLite3 / PostgreSQL)             │
└─────────────────────────────────────────────┘
```

## 快速开始

### 环境要求
- Python 3.8+
- Django 5.0
- Pillow
- qrcode

### 一键启动 (Windows)
1. 双击运行 `start.bat` 或 `quick_start.bat`
2. 系统将自动：
   - 创建虚拟环境
   - 安装依赖包
   - 运行数据库迁移
   - 创建管理员账号
   - 启动开发服务器

### 手动安装步骤

#### 1. 克隆项目
```bash
git clone <项目地址>
cd Farm_Management_System-main
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
```

#### 3. 激活虚拟环境
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 4. 安装依赖
```bash
pip install django==5.0 pillow qrcode qrcode[pil] -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 5. 数据库配置
```bash
python manage.py migrate
```

#### 6. 创建管理员账号
```bash
python manage.py createsuperuser
```
- 用户名: admin
- 密码: 123456
- 邮箱: admin@kuerle-pear.com

#### 7. 启动开发服务器
```bash
python manage.py runserver 8080
```

#### 8. 访问系统
- 打开浏览器访问: http://127.0.0.1:8080
- 管理员登录: http://127.0.0.1:8080/admin

### 测试数据
系统提供了测试数据脚本，可以快速生成演示数据：
```bash
python add_test_data.py
```
或
```bash
python seed_data.py
```

## 系统配置

### 基础配置
在 `FarmManagementSystem/settings.py` 中配置：
```python
# 允许的主机
ALLOWED_HOSTS = ['*']

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 媒体文件配置
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 安全配置
```python
# 生产环境需要修改
DEBUG = True
SECRET_KEY = 'your-secret-key-here'

# 安全设置
SECURE_SSL_REDIRECT = False  # 生产环境设为True
SESSION_COOKIE_SECURE = False  # 生产环境设为True
CSRF_COOKIE_SECURE = False  # 生产环境设为True
```

### 二维码配置
```python
# 二维码生成设置
QR_CODE_SIZE = 10
QR_CODE_BORDER = 4
QR_CODE_FILL_COLOR = "black"
QR_CODE_BACK_COLOR = "white"

# 溯源链接格式
TRACE_URL_FORMAT = "http://127.0.0.1:8080/trace/{serial_number}/"
```

## 数据管理

### 数据模型
系统包含以下核心数据模型：

#### 1. 种植管理
- `Crops`: 香梨种植地块
- `Crop_expenses`: 种植费用
- `Crop_sales`: 销售记录
- `Crop_operations`: 种植操作

#### 2. 采摘批次
- `Livestock`: 采摘批次（重命名为物流追踪记录）
- `Livestock_production`: 生产记录

#### 3. 二维码管理
- `QRCodeBatch`: 二维码批次
- `QRCodeScanLog`: 二维码扫描日志

#### 4. 物流追踪
- `LogisticsTracking`: 物流追踪记录
- `Storage`: 仓储管理
- `StorageItem`: 仓储物品

#### 5. 系统管理
- `Employees`: 员工信息
- `Machinery`: 机械设备
- `Milk_production`: 产量记录（示例）
- `Eggs_production`: 禽蛋记录（示例）

### 数据关系
```
Crops (种植地块)
  ├── Crop_expenses (费用)
  ├── Crop_sales (销售)
  └── Crop_operations (操作)

Livestock (采摘批次)
  ├── Livestock_production (生产记录)
  ├── QRCodeBatch (二维码)
  │   └── QRCodeScanLog (扫描日志)
  ├── LogisticsTracking (物流记录)
  └── StorageItem (仓储物品)
      └── Storage (仓库)
```

### 数据导入导出
系统支持以下数据操作：
- **CSV导入**: 批量导入种植、批次数据
- **Excel导出**: 导出统计报表
- **JSON API**: 提供数据接口
- **数据备份**: 定期备份数据库

## 部署说明

### 开发环境
- **操作系统**: Windows 10/11, macOS, Linux
- **Python版本**: 3.8+
- **数据库**: SQLite3
- **Web服务器**: Django开发服务器

### 生产环境
- **操作系统**: Ubuntu Server 20.04 LTS
- **Python版本**: 3.8+
- **数据库**: PostgreSQL 13+
- **Web服务器**: Nginx + Gunicorn
- **反向代理**: Nginx
- **进程管理**: Systemd

### Docker部署
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "FarmManagementSystem.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 云部署
- **阿里云**: ECS + RDS + OSS
- **腾讯云**: CVM + CDB + COS
- **AWS**: EC2 + RDS + S3

## 开发指南

### 项目结构
```
Farm_Management_System-main/
├── FarmManagementSystem/     # Django项目配置
│   ├── settings.py          # 系统设置
│   ├── urls.py             # 主URL配置
│   └── wsgi.py             # WSGI配置
├── homepage/               # 主应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── urls.py            # 应用URL
│   ├── templates/         # 模板文件
│   └── migrations/        # 数据库迁移
├── authentication/         # 认证应用
├── static/                # 静态文件
├── media/                 # 媒体文件
├── db.sqlite3             # 数据库
├── manage.py              # Django管理脚本
└── requirements.txt       # 依赖包列表
```

### 开发流程
1. **环境搭建**: 按照快速开始步骤配置开发环境
2. **功能开发**: 在对应应用中添加模型、视图、模板
3. **数据库迁移**: 修改模型后运行迁移命令
4. **测试验证**: 使用测试数据验证功能
5. **代码提交**: 遵循Git工作流提交代码

### API接口
系统提供以下REST API接口：
- `GET /api/crops/`: 获取种植地块列表
- `GET /api/livestock/`: 获取采摘批次列表
- `GET /api/qrcodes/`: 获取二维码列表
- `GET /api/logistics/`: 获取物流记录
- `GET /api/trace/{serial_number}/`: 溯源查询接口

### 测试脚本
系统包含以下测试脚本：
- `add_test_data.py`: 生成测试数据
- `seed_data.py`: 种子数据脚本
- `test_api.py`: API接口测试

## 许可证

本项目基于MIT许可证开源，详情请查看 [MIT_license](MIT_license) 文件。

## 联系我们

### 项目维护
- **项目名称**: 库尔勒香梨生产溯源管理系统
- **版本**: 1.0.0
- **最后更新**: 2024年2月

### 技术支持
- **问题反馈**: 请提交GitHub Issues
- **功能建议**: 欢迎提交Pull Request
- **技术咨询**: 通过邮件联系我们

### 致谢
感谢所有为项目做出贡献的开发者和测试人员，特别感谢库尔勒香梨产业协会的技术支持和业务指导。

---
**让每一颗香梨都有故事，让每一次消费都更安心**