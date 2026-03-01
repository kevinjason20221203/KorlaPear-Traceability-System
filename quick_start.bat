@echo off
echo 库尔勒香梨生产溯源管理系统 - 快速启动
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate
python manage.py runserver 8080

pause