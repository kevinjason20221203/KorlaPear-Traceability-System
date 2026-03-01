@echo off
echo ========================================
echo 库尔勒香梨生产溯源管理系统 - 启动脚本
echo ========================================
echo.

REM 检查是否在项目根目录
if not exist "manage.py" (
    echo 错误：请在项目根目录运行此脚本！
    echo 当前目录：%cd%
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo 警告：虚拟环境不存在！
    echo 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo 错误：创建虚拟环境失败！
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功！
    echo.
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate
if errorlevel 1 (
    echo 错误：激活虚拟环境失败！
    pause
    exit /b 1
)

REM 检查依赖
echo 检查Python依赖...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo 依赖未安装，正在安装...
    pip install django==5.0 pillow qrcode qrcode[pil] -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo 错误：安装依赖失败！
        pause
        exit /b 1
    )
    echo 依赖安装成功！
)

REM 检查数据库
echo 检查数据库...
python manage.py check >nul 2>&1
if errorlevel 1 (
    echo 数据库检查失败，正在修复...
    python manage.py migrate
    if errorlevel 1 (
        echo 错误：数据库迁移失败！
        pause
        exit /b 1
    )
    echo 数据库修复成功！
)

REM 检查端口占用
echo 检查8080端口...
netstat -ano | findstr :8080 >nul
if not errorlevel 1 (
    echo 警告：8080端口已被占用！
    echo 正在清理占用进程...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080') do (
        taskkill /f /pid %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
    echo 端口清理完成！
)

REM 启动服务器
echo.
echo ========================================
echo 正在启动服务器...
echo ========================================
echo.
echo 访问地址：http://127.0.0.1:8080
echo 管理员账号：admin / 123456
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver 8080

REM 服务器停止后的处理
echo.
echo ========================================
echo 服务器已停止
echo ========================================
echo.
pause