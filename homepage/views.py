from django.shortcuts import render, redirect


# Create your views here.
def Mainpage(request):
    return render(request, "homepage/home.html")


# views for the employees
from .employees_form import EmployeesForm
from .models import Employees


def Show_employees(request):
    # 显示所有员工数据（临时修复：显示所有数据）
    employees = Employees.objects.all()
    print(f"DEBUG: 查询到 {employees.count()} 名员工")
    
    return render(request, "homepage/showemployees.html", {"employees": employees})


def Add_employees(request):
    if request.method == "POST":
        form = EmployeesForm(request.POST)
        if form.is_valid():
            employees = form.save(commit=False)
            employees.user = request.user

            form.save()

            return redirect("homepage:show-employees")

    else:
        form = EmployeesForm()
    return render(request, "homepage/addemployees.html", {"form": form})


def Delete_employees(request, Eid):
    employees = Employees.objects.get(Eid=Eid)
    if request.method == "POST":
        employees.delete()
        return redirect("homepage:show-employees")

    return render(request, "homepage/deleteemployees.html", {"employees": employees})


def Update_employees(request, Eid):
    employees = Employees.objects.get(Eid=Eid)
    form = EmployeesForm(request.POST, instance=employees)

    if form.is_valid():
        form.save()
        return redirect("homepage:show-employees")

    return render(request, "homepage/updateemployees.html", {"employees": employees})


# views for crops
from .models import Crops,Crop_expenses,Crop_sales,Crop_operations
from .crops_form import CropsForm,Crop_expensesForm,Crop_salesForm,Crop_operationsForm


def Show_crops(request):
    # 显示所有种植档案数据（临时修复：显示所有数据）
    crops = Crops.objects.all()
    print(f"DEBUG: 查询到 {crops.count()} 个种植地块")
    
    return render(request, "homepage/showcrops.html", {"crops": crops})


def Add_crops(request):
    if request.method == "POST":
        form = CropsForm(request.POST)
        if form.is_valid():
            crops = form.save(commit=False)
            crops.user = request.user
            form.save()

            return redirect("homepage:show-crops")
    else:
        form = CropsForm()

    return render(request, "homepage/addcrops.html", {"form": form})


def Update_crops(request, Cid):
    crops = Crops.objects.get(Cid=Cid)
    form = CropsForm(request.POST, instance=crops)

    if form.is_valid():
        form.save()
        return redirect("homepage:show-crops")
    
    else:
        print(form.errors)

    return render(request, "homepage/updatecrops.html", {"crops": crops})

def Delete_crops (request,Cid):
    crops=Crops.objects.get(Cid=Cid)
    if request.method =="POST":
        crops.delete()
        return redirect("homepage:show-crops")
    
    return render(request,'homepage/deletecrops.html', {'crops':crops})

def Show_crop_expenses(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    expenses=Crop_expenses.objects.filter(crops=crops)

    return render(request,'homepage/showcropexpenses.html',{'crops':crops,'expenses':expenses})

def Add_crop_expenses(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method=='POST':
        form=Crop_expensesForm(request.POST)
        if form.is_valid():
            crop_expense=form.save(commit=False)
            crop_expense.crops=crops
            crop_expense.save()
            return redirect('homepage:show-cropexpenses', Cid=crops.Cid)
        
    else:
        form = Crop_expensesForm()
        return render(request,'homepage/addcropexpenses.html',{'form':form, 'crops':crops})
    

def Update_crop_expenses(request,Cid,Expense_date):
    crops=get_object_or_404(Crops,Cid=Cid)
    crop_expenses=get_object_or_404(Crop_expenses,crops__Cid=Cid,Expense_date=Expense_date)
    form=Crop_expensesForm(request.POST,instance=crop_expenses)

    if form.is_valid():
        form.save()
        return redirect('homepage:show-cropexpenses',Cid=crop_expenses.crops.Cid)
    else:
        print(form.errors)

    return render(request,'homepage/updatecropexpenses.html',{'crops':crops,'crop_expenses':crop_expenses})

def Delete_crop_expenses(request,Cid,Expense_date):
    crop_expenses=get_object_or_404(Crop_expenses, crops__Cid=Cid,Expense_date=Expense_date)
    if request.method=="POST":
        Crop_expenses.delete()
        return redirect('homepage:show-cropexpenses ',Cid=crop_expenses.crops.Cid)
    
    return render(request,'homepage/deletecropexpenses.html',{'crop_expenses':crop_expenses})
    

def Show_crop_sales(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    sales=Crop_sales.objects.filter(crops=crops)

    return render(request,"homepage/showcropsales.html",{'crops':crops,'sales':sales})

def Add_crop_sales(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method =='POST':
        form=Crop_salesForm(request.POST)
        if form.is_valid():
            crop_sale=form.save(commit=False)
            crop_sale.crops=crops
            crop_sale.save()
            return redirect('homepage:show-cropsales', Cid=crops.Cid)
        
    else:
        form=Crop_salesForm()
    return render(request,'homepage/addcropsales.html', {'form':form, 'crops':crops})
    

def Delete_crop_sales(request,Cid,Sale_date):
    crop_sales=get_object_or_404(Crop_sales,crops__Cid=Cid,Sale_date=Sale_date)

    if request.method=='POST':
        crop_sales.delete()
        return redirect('homepage:show-cropsales', Cid=crop_sales.crops.Cid)
    return render(request,'homepage/deletecropsales.html',{'crop_sales':crop_sales})

def Update_crop_sales(request,Cid,Sale_date):
    crops= get_object_or_404(Crops,Cid=Cid)
    crop_sales=get_object_or_404(Crop_sales,crops__Cid=Cid,Sale_date=Sale_date)
    form=Crop_salesForm(request.POST,instance=crop_sales)

    if form.is_valid():
        form.save()

        return redirect('homepage:show-cropsales', Cid=crop_sales.crops.Cid)
    
    else:
        print(form.errors)

    return render(request,'homepage/updatecropsales.html',{'crops':crops,'crop_sales':crop_sales})

def Show_crop_operations(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    operations=Crop_operations.objects.filter(crops=crops)

    return render(request,'homepage/showcropoperations.html',{'crops':crops, 'operations':operations})

def Add_crop_operations(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method=='POST':
        form=Crop_operationsForm(request.POST)
        if form.is_valid():
            crop_operation=form.save(commit=False)
            crop_operation.crops=crops
            crop_operation.save()
            return redirect('homepage:show-cropoperations',Cid=crops.Cid)
    else:
        form=Crop_operationsForm()
        return render(request, 'homepage/addcropoperations.html',{'form':form,'crops':crops})

def Delete_crop_operations(request,Cid,Operation_date):
    crop_operations=get_object_or_404(Crop_operations,crops__Cid=Cid,Operation_date=Operation_date)
    if request.method=='POST':
        crop_operations.delete()
        return redirect('homepage:show-cropoperations',Cid=crop_operations.crops.Cid)
    
    return render(request, 'homepage/deletecropoperations.html',{'crop_operations':crop_operations})


def Update_crop_operations(request,Cid,Operation_date):
    crops= get_object_or_404(Crops,Cid=Cid)
    crop_operations=get_object_or_404(Crop_operations,crops__Cid=Cid,Operation_date=Operation_date)
    form  = Crop_operationsForm(request.POST,instance=crop_operations)

    if form.is_valid():
        form.save()

        return redirect('homepage:show-cropoperations',Cid=crop_operations.crops.Cid)
    
    return render(request,'homepage/updatecropoperations.html',{'crops':crops,'crop_operations':crop_operations})
    
    
    

#views for the Machinery

from .models import Machinery,Machinery_activities,Machinery_maintenance
from .machinery_form import MachineryForm,Machinery_activitesForm,Machinery_maintenanceForm

def Show_machinery(request):
    # 显示所有农机设备数据（临时修复：显示所有数据）
    machinery = Machinery.objects.all()
    print(f"DEBUG: 查询到 {machinery.count()} 台农机设备")
    
    return render(request, "homepage/showmachinery.html", {'machinery':machinery})


def Add_machinery(request):
    if request.method=='POST':
        form = MachineryForm(request.POST)
        if form.is_valid():
            machinery= form.save(commit=False)
            machinery.user =request.user
            form.save()
            return redirect("homepage:show-machinery")
        
    else:
        form = MachineryForm()

        return render(request,"homepage/addmachinery.html", {"form":form})


def Delete_machinery(request,Number_plate):
    machinery=Machinery.objects.get(Number_plate=Number_plate)
    if request.method=="POST":
        machinery.delete()
        return redirect("homepage:show-machinery")
        
    return render(request,"homepage/deletemachinery.html", {"machinery":machinery})


def Update_machinery(request,Number_plate):
    machinery=Machinery.objects.get(Number_plate=Number_plate)
    form = MachineryForm(request.POST, instance=machinery)

    if form.is_valid():
        form.save()
        return redirect("homepage:show-machinery")
    
    else:
        print(form.errors)
    
    return render(request, "homepage/updatemachinery.html", {'machinery':machinery})


def Show_machinery_activities(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    activities=Machinery_activities.objects.filter(machinery=machinery)
    return render(request, 'homepage/showmachineryactivities.html',{'machinery':machinery,'activities':activities})

def Add_machinery_activities(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)

    if request.method=='POST':
        form=Machinery_activitesForm(request.POST)
        if form.is_valid():
            machinery_activity=form.save(commit=False)
            machinery_activity.machinery=machinery
            machinery_activity.save()
            return redirect('homepage:show-machineryactivities', Number_plate=machinery.Number_plate)
        

    else:
        form=Machinery_activitesForm()
    return render(request, 'homepage/addmachineryactivities.html',{'machinery':machinery,'form':form})

def Delete_machinery_activity(request,Number_plate,Activity_date):
    machinery_activities=get_object_or_404(Machinery_activities,machinery__Number_plate=Number_plate,Activity_date=Activity_date)
    if request.method=='POST':
        machinery_activities.delete()
        return redirect('homepage:show-machineryactivities',Number_plate=machinery_activities.machinery.Number_plate)
    
    return render(request,'homepage/deletemachineryactivities.html',{'machinery_activities':machinery_activities})


def Update_machinery_activities(request,Number_plate,Activity_date):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    machinery_activities=get_object_or_404(Machinery_activities,machinery__Number_plate=Number_plate,Activity_date=Activity_date)
    form=Machinery_activitesForm(request.POST,instance=machinery_activities)

    if form.is_valid():
        form.save()
        return redirect('homepage:show-machineryactivities',Number_plate=machinery_activities.machinery.Number_plate)
    
    return render(request,'homepage/updatemachineryactivities.html',{'machinery':machinery,'machinery_activities':machinery_activities})

def Show_machinery_maintenance(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    maintenance=Machinery_maintenance.objects.filter(machinery=machinery)
    return render(request,'homepage/showmachinerymaintenance.html',{'machinery':machinery,'maintenance':maintenance})

def Add_machinery_maintenance(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)

    if request.method=='POST':
        form=Machinery_maintenanceForm(request.POST)
        if form.is_valid():
            machinery_maintenance=form.save(commit=False)
            machinery_maintenance.machinery=machinery
            machinery_maintenance.save()
            return redirect('homepage:show-machinerymaintenance',Number_plate=machinery.Number_plate)
        
    else:
        form=Machinery_maintenanceForm()
    return render(request, 'homepage/addmachinerymaintenance.html',{'machinery':machinery,'form':form})

def Delete_machinery_maintenance(request,Number_plate,Date):
    machinery_maintenance=get_object_or_404(Machinery_maintenance,machinery__Number_plate=Number_plate,Date=Date)
    if request.method=='POST':
        machinery_maintenance.delete()
        return redirect('homepage:show-machinerymaintenance',Number_plate=machinery_maintenance.machinery.Number_plate)
    
    return render(request,'homepage/deletemachinerymaintenance.html',{'machinery_maintenance':machinery_maintenance})


def Update_machinery_maintenance(request,Number_plate,Date):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    machinery_maintenance=get_object_or_404(Machinery_maintenance,machinery__Number_plate=Number_plate,Date=Date)
    form=Machinery_maintenanceForm(request.POST,instance=machinery_maintenance)

    if form.is_valid():
        form.save()
        return redirect('homepage:show-machinerymaintenance',Number_plate=machinery_maintenance.machinery.Number_plate)
    
    return render(request,'homepage/updatemachinerymaintenance.html',{'machinery':machinery,'machinery_maintenance':machinery_maintenance})
    


#view function of the livestock section
from .livestock_form import LivestockForm,Livestock_productionForm,Milk_productionForm,Egg_productionForm
from .models import Livestock,Livestock_production,Milk_production,Eggs_production
from django.shortcuts import render, get_object_or_404

def Show_livestock(request):
    # 显示所有采摘批次数据（临时修复：显示所有数据）
    livestock = Livestock.objects.all()
    print(f"DEBUG: 查询到 {livestock.count()} 个采摘批次")
    
    return render(request,"homepage/showlivestock.html", {'livestock':livestock})


def Add_livestock(request):
    if request.method=="POST":
        form=LivestockForm(request.POST)
        if form.is_valid():
            livestock=form.save(commit=False)
            livestock.user = request.user

            form.save()

            return redirect("homepage:show-livestock")
        
    else:
        form = LivestockForm()
        return render(request,"homepage/addlivestock.html", {'form':form})
    

def Update_livestock(request,Tag_number):
    livestock=Livestock.objects.get(Tag_number=Tag_number)
    form = LivestockForm(request.POST,instance=livestock)

    if form.is_valid():
        form.save()
        return redirect("homepage:show-livestock")
    
    else:
        print(form.errors)

    return render(request,"homepage/updatelivestock.html",{'livestock':livestock})

def Delete_livestock(request,Tag_number):
    livestock=Livestock.objects.get(Tag_number=Tag_number)
    if request.method=="POST":
        livestock.delete()
        return redirect("homepage:show-livestock")
    
    return render(request, "homepage/deletelivestock.html", {'livestock':livestock})

def Show_livestock_production(request, Tag_number):
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    productions = Livestock_production.objects.filter(livestock=livestock)

    return render(request, 'homepage/showlivestockproduction.html', {'livestock': livestock, 'productions': productions})


def Add_livestock_production(request, Tag_number):
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)

    if request.method == 'POST':
        form = Livestock_productionForm(request.POST)
        if form.is_valid():
            livestock_production = form.save(commit=False)
            livestock_production.livestock = livestock
            livestock_production.save()
            return redirect('homepage:show-livestockproduction', Tag_number=livestock.Tag_number)
    else:
        form = Livestock_productionForm()

        return render(request, 'homepage/addlivestockproduction.html', {'form': form, 'livestock': livestock})
    

def Delete_livestock_production(request,Tag_number,Production_date):
    livestock_production = get_object_or_404(Livestock_production,livestock__Tag_number=Tag_number,Production_date=Production_date)
    if request.method=="POST":
        livestock_production.delete()
        return redirect("homepage:show-livestockproduction",  Tag_number=livestock_production.livestock.Tag_number)
    
    return render(request, 'homepage/deletelivestockproduction.html',{'livestock_production':livestock_production})

def Update_livestock_production(request,Tag_number,Production_date):
    livestock=get_object_or_404(Livestock,Tag_number=Tag_number)
    livestock_production=get_object_or_404(Livestock_production,livestock__Tag_number=Tag_number,Production_date=Production_date)
    form=Livestock_productionForm(request.POST,instance=livestock_production)

    if form.is_valid():
        form.save()
        return redirect('homepage:show-livestockproduction', Tag_number=livestock_production.livestock.Tag_number)
    else:
        print(form.errors)

    return render(request,'homepage/updatelivestockproduction.html',{'livestock':livestock, 'livestock_production':livestock_production})



# the milk production section in the dashboard

def Select_year_month(request):
    if request.method=='POST':
        selected_year=request.POST.get('Year')
        selected_month=request.POST.get('Month')
        return redirect('homepage:milk-productionbymonth',selected_year=selected_year,selected_month=selected_month)
    return render(request,'homepage/selectyearmonth.html')

# views.py
import matplotlib
matplotlib.use('Agg') #rendering the graphs that does not use tikinter in order to remove the tikinter error
import matplotlib.pyplot as plt
from io import BytesIO # create an in-memory buffer to temporarily store the binary data of the generated plots.
import base64 # encode the binary data of the plots into Base64 format(Base64 encoding used to convert binary data into  such as images, into a text-based format that can be easily embedded in HTML)

def Milk_production_by_month(request, selected_year, selected_month):
    # Fetching milk production by the year and month selected
    milk_production_records = Milk_production.objects.filter(Year=selected_year, Month=selected_month)

    # Prepare data for the bar graph of total consumption vs day
    days = [record.Day  for record in milk_production_records]
    total_consumption = [record.Total_consumption for record in milk_production_records]

    # Create a bar graph for Total Consumption vs Day
    plt.figure(figsize=(12, 6))
    plt.bar(days, total_consumption, color='green')
    plt.title('Total Consumption vs Day')
    plt.xlabel('Day')
    plt.ylabel('Total Consumption')
    
    # Save the plot to a BytesIO object
    image_stream_consumption = BytesIO()
    plt.savefig(image_stream_consumption, format='png')
    image_stream_consumption.seek(0)
    image_base64_consumption = base64.b64encode(image_stream_consumption.read()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    # Prepare data for the bar graph of milk production vs day
    total_production = [record.Total_production for record in milk_production_records]

    # Create a bar graph for Milk Production vs Day
    plt.figure(figsize=(12, 6))
    plt.bar(days, total_production, color='blue')
    plt.title('Milk Production vs Day')
    plt.xlabel('Day')
    plt.ylabel('Milk Production')

    # Save the plot to a BytesIO object
    image_stream_production = BytesIO()
    plt.savefig(image_stream_production, format='png')
    image_stream_production.seek(0)
    image_base64_production = base64.b64encode(image_stream_production.read()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    # Pass both base64-encoded images to the template
    return render(request, 'homepage/milkproductionbymonth.html', {
        'selected_year': selected_year,
        'selected_month': selected_month,
        'image_base64_consumption': image_base64_consumption,
        'image_base64_production': image_base64_production,
        'milk_production_records': milk_production_records,
    })


def Add_milk_production_by_month(request,selected_year,selected_month):
    if request.method=='POST':
        form=Milk_productionForm(request.POST)
        if form.is_valid():
            production=form.save(commit=False)
            production.Year=selected_year
            production.Month=selected_month
            production.save()
            return redirect('homepage:milk-productionbymonth',selected_year=selected_year,selected_month=selected_month)

    else:
        form=Milk_productionForm()

    return render(request,'homepage/addmilkproduction.html',{'form':form,'selected_year':selected_year,'selected_month':selected_month})



def Delete_milk_production_by_month(request,selected_year,selected_month,Day):
    milk_production_records=get_object_or_404(Milk_production,Day=Day)
    if request.method=='POST':
        milk_production_records.delete()
        return redirect('homepage:milk-productionbymonth', selected_year=selected_year,selected_month=selected_month)
    
    return render(request, 'homepage/deletemilkproduction.html', {'milk_production_records':milk_production_records,'selected_year':selected_year,'selected_month':selected_month})

def Update_milk_production_by_month(request,selected_year,selected_month,Day):
    milk_production_record=get_object_or_404(Milk_production,Day=Day,Year=selected_year,Month=selected_month)
    form=Milk_productionForm(request.POST,instance=milk_production_record)

    if form.is_valid():
        form.save()
        return redirect('homepage:milk-productionbymonth', selected_year=selected_year,selected_month=selected_month)
    
    else:
        print(form.errors)

    return render(request,'homepage/updatemilkproduction.html',{'milk_production_record':milk_production_record, 'selected_year':selected_year,'selected_month':selected_month})

#Eggs production
def Select_year_month_egg(request):
    if request.method=='POST':
        selected_year=request.POST.get('Year')
        selected_month=request.POST.get('Month')

        return redirect('homepage:egg-productionrecord', selected_year=selected_year, selected_month=selected_month)
        
    return render(request,'homepage/selectingyearandmonth.html' )


def Egg_production_record(request,selected_year, selected_month):
    egg_production_records=Eggs_production.objects.filter(Year=selected_year,Month=selected_month)
    
    # 为每个记录添加溯源码状态和质量等级（演示数据）
    enhanced_records = []
    for record in egg_production_records:
        # 模拟溯源码状态：已生成/未生成
        trace_code_status = "已生成" if record.Day % 2 == 0 else "未生成"
        
        # 模拟质量等级：特级/一级/二级
        quality_grades = ["特级", "一级", "二级"]
        quality_grade = quality_grades[record.Day % 3]
        
        # 模拟批次号
        batch_number = f"KRL-{selected_year}{selected_month:02d}{record.Day:02d}-001"
        
        # 将额外信息添加到记录中
        record.trace_code_status = trace_code_status
        record.quality_grade = quality_grade
        record.batch_number = batch_number
        
        enhanced_records.append(record)

    return render(request,'homepage/showeggproduction.html', {
        'egg_production_records': enhanced_records, 
        'selected_year': selected_year, 
        'selected_month': selected_month
    })

def Add_egg_production_by_month(request,selected_year,selected_month):
    if request.method=='POST':
        form=Egg_productionForm(request.POST)
        if form.is_valid():
            production=form.save(commit=False)
            production.Year=selected_year
            production.Month=selected_month
            production.save()
            return redirect('homepage:egg-productionrecord', selected_year=selected_year,selected_month=selected_month)
    else:
        form=Egg_productionForm()
    return render(request, 'homepage/addeggproduction.html', {'form':form,'selected_year':selected_year,'selected_month':selected_month})

def Delete_egg_production_by_month(request,selected_year,selected_month,Day):
    egg_production_records=get_object_or_404(Eggs_production,Day=Day)
    if request.method=='POST':
        egg_production_records.delete()
        return redirect('homepage:egg-productionrecord', selected_year=selected_year,selected_month=selected_month)
    return render(request, 'homepage/deleteeggproduction.html', {'egg_production_records':egg_production_records,'selected_year':selected_year,'selected_month':selected_month})

def Update_egg_production_by_month(request,selected_year,selected_month,Day):
    egg_production_record=get_object_or_404(Eggs_production,Day=Day,Year=selected_year,Month=selected_month)
    form=Egg_productionForm(request.POST,instance=egg_production_record)

    if form.is_valid():
        form.save()
        return redirect('homepage:egg-productionrecord',selected_year=selected_year,selected_month=selected_month)
    else:
        print(form.errors)

    return render(request,'homepage/updateeggproduction.html',{'egg_production_record':egg_production_record,'selected_year':selected_year,'selected_month':selected_month})

def Help(request):
    return render(request, 'homepage/help.html')

def settings_view(request):
    """系统设置页面"""
    return render(request, 'homepage/settings.html')


# ==================== 二维码批次管理模块 ====================

from .models import QRCodeBatch, QRCodeScanLog
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def generate_qrcode_for_livestock(request, Tag_number):
    """为采摘批次生成二维码"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    from django.shortcuts import get_object_or_404
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    
    # 检查是否已存在二维码
    existing_qrcode = QRCodeBatch.objects.filter(livestock=livestock).first()
    
    if existing_qrcode:
        # 如果已存在，返回现有二维码
        return render(request, 'homepage/show_qrcode.html', {
            'qrcode': existing_qrcode,
            'livestock': livestock,
            'message': '该采摘批次已有二维码'
        })
    
    # 创建新的二维码
    qrcode = QRCodeBatch.objects.create(
        user=request.user,
        livestock=livestock,
        qr_content=f"http://127.0.0.1:8080/trace/{livestock.Tag_number}/"
    )
    
    return render(request, 'homepage/show_qrcode.html', {
        'qrcode': qrcode,
        'livestock': livestock,
        'message': '二维码生成成功'
    })

def show_qrcode_list(request):
    """显示所有二维码列表"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    qrcodes = QRCodeBatch.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'homepage/qrcode_list.html', {'qrcodes': qrcodes})

def qrcode_scanner(request):
    """二维码扫描页面"""
    return render(request, 'homepage/qrcode_scanner.html')

@csrf_exempt
def process_qrcode_scan(request):
    """处理二维码扫描（API接口）"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serial_number = data.get('serial_number')
            scanner_ip = request.META.get('REMOTE_ADDR')
            scan_type = data.get('scan_type', 'consumer')
            scanner_location = data.get('scanner_location', '')
            
            # 查找二维码
            qrcode = QRCodeBatch.objects.get(serial_number=serial_number)
            
            # 更新最后扫描时间
            qrcode.last_scanned = timezone.now()
            qrcode.status = 'scanned'
            qrcode.save()
            
            # 记录扫描日志
            QRCodeScanLog.objects.create(
                qr_code=qrcode,
                scanner_ip=scanner_ip,
                scanner_location=scanner_location,
                scan_type=scan_type
            )
            
            # 返回二维码关联的采摘批次信息
            livestock = qrcode.livestock
            response_data = {
                'success': True,
                'serial_number': serial_number,
                'livestock': {
                    'tag_number': livestock.Tag_number,
                    'animal_type': livestock.Animal_type,
                    'age': livestock.Age,
                    'breed': livestock.Breed
                },
                'scan_time': timezone.now().isoformat(),
                'message': '二维码扫描成功'
            }
            
            return JsonResponse(response_data)
            
        except QRCodeBatch.DoesNotExist:
            return JsonResponse({'success': False, 'error': '二维码不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': '只支持POST请求'}, status=400)

def trace_query(request, serial_number):
    """溯源查询页面（公开访问）"""
    try:
        qrcode = QRCodeBatch.objects.get(serial_number=serial_number)
        livestock = qrcode.livestock
        
        # 获取关联的种植地块信息
        # 注意：Livestock模型目前没有直接关联Crops，需要根据业务逻辑调整
        # 这里假设Livestock的Tag_number包含相关信息
        
        # 获取扫描日志
        scan_logs = QRCodeScanLog.objects.filter(qr_code=qrcode).order_by('-scanned_at')
        
        return render(request, 'homepage/trace_query.html', {
            'qrcode': qrcode,
            'livestock': livestock,
            'scan_logs': scan_logs,
            'scan_count': scan_logs.count()
        })
        
    except QRCodeBatch.DoesNotExist:
        return render(request, 'homepage/trace_query.html', {
            'error': '溯源码不存在或已失效',
            'serial_number': serial_number
        })

def qrcode_management(request, Tag_number):
    """二维码管理页面"""
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    qrcodes = QRCodeBatch.objects.filter(livestock=livestock)
    
    return render(request, 'homepage/qrcode_management.html', {
        'livestock': livestock,
        'qrcodes': qrcodes
    })


# ==================== 物流追踪系统模块 ====================

from .models import LogisticsTracking, Storage, StorageItem
from django.utils import timezone

def show_logistics_tracking(request, Tag_number):
    """显示采摘批次的物流追踪记录"""
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    tracking_records = LogisticsTracking.objects.filter(livestock=livestock).order_by('-timestamp')
    
    return render(request, 'homepage/show_logistics_tracking.html', {
        'livestock': livestock,
        'tracking_records': tracking_records,
        'record_count': tracking_records.count()
    })

def add_logistics_tracking(request, Tag_number):
    """添加物流追踪记录"""
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        location = request.POST.get('location')
        location_type = request.POST.get('location_type')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        operation_notes = request.POST.get('operation_notes')
        
        # 创建物流追踪记录
        tracking = LogisticsTracking.objects.create(
            user=request.user,
            livestock=livestock,
            status=status,
            location=location,
            location_type=location_type,
            temperature=float(temperature) if temperature else None,
            humidity=float(humidity) if humidity else None,
            operator=request.user,
            operation_notes=operation_notes,
            timestamp=timezone.now()
        )
        
        return redirect('homepage:show-logistics-tracking', Tag_number=livestock.Tag_number)
    
    return render(request, 'homepage/add_logistics_tracking.html', {
        'livestock': livestock,
        'status_choices': LogisticsTracking.STATUS_CHOICES,
        'location_type_choices': LogisticsTracking._meta.get_field('location_type').choices
    })

def show_storage_list(request):
    """显示仓库列表"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    storages = Storage.objects.filter(user=request.user)
    
    return render(request, 'homepage/show_storage_list.html', {
        'storages': storages
    })

def add_storage(request):
    """添加仓库"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    if request.method == 'POST':
        storage_name = request.POST.get('storage_name')
        storage_type = request.POST.get('storage_type')
        capacity = request.POST.get('capacity')
        address = request.POST.get('address')
        manager_name = request.POST.get('manager_name')
        contact_phone = request.POST.get('contact_phone')
        optimal_temperature = request.POST.get('optimal_temperature')
        optimal_humidity = request.POST.get('optimal_humidity')
        
        storage = Storage.objects.create(
            user=request.user,
            storage_name=storage_name,
            storage_type=storage_type,
            capacity=float(capacity),
            address=address,
            manager_name=manager_name,
            contact_phone=contact_phone,
            optimal_temperature=float(optimal_temperature) if optimal_temperature else None,
            optimal_humidity=float(optimal_humidity) if optimal_humidity else None
        )
        
        return redirect('homepage:show-storage-list')
    
    return render(request, 'homepage/add_storage.html', {
        'storage_type_choices': Storage._meta.get_field('storage_type').choices
    })

def show_storage_detail(request, storage_id):
    """显示仓库详情"""
    storage = get_object_or_404(Storage, id=storage_id)
    storage_items = StorageItem.objects.filter(storage=storage, is_in_storage=True)
    
    return render(request, 'homepage/show_storage_detail.html', {
        'storage': storage,
        'storage_items': storage_items,
        'usage_percentage': storage.get_usage_percentage()
    })

def add_storage_item(request, storage_id):
    """添加仓储物品"""
    storage = get_object_or_404(Storage, id=storage_id)
    
    if request.method == 'POST':
        livestock_id = request.POST.get('livestock')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        quality_grade = request.POST.get('quality_grade')
        storage_temperature = request.POST.get('storage_temperature')
        storage_humidity = request.POST.get('storage_humidity')
        notes = request.POST.get('notes')
        
        livestock = get_object_or_404(Livestock, Tag_number=livestock_id)
        
        storage_item = StorageItem.objects.create(
            storage=storage,
            livestock=livestock,
            quantity=float(quantity),
            unit_price=float(unit_price),
            quality_grade=quality_grade,
            storage_temperature=float(storage_temperature) if storage_temperature else None,
            storage_humidity=float(storage_humidity) if storage_humidity else None,
            notes=notes
        )
        
        # 更新仓库使用量
        storage.current_usage += float(quantity)
        storage.save()
        
        return redirect('homepage:show-storage-detail', storage_id=storage.id)
    
    # 获取可用的采摘批次（尚未入库的）
    available_livestock = Livestock.objects.filter(
        user=request.user
    ).exclude(
        id__in=StorageItem.objects.filter(is_in_storage=True).values('livestock_id')
    )
    
    return render(request, 'homepage/add_storage_item.html', {
        'storage': storage,
        'available_livestock': available_livestock,
        'quality_grade_choices': StorageItem._meta.get_field('quality_grade').choices
    })

def remove_storage_item(request, item_id):
    """出库操作"""
    storage_item = get_object_or_404(StorageItem, id=item_id)
    storage = storage_item.storage
    
    if request.method == 'POST':
        # 更新出库时间
        storage_item.date_removed = timezone.now()
        storage_item.is_in_storage = False
        storage_item.save()
        
        # 更新仓库使用量
        storage.current_usage -= storage_item.quantity
        if storage.current_usage < 0:
            storage.current_usage = 0
        storage.save()
        
        return redirect('homepage:show-storage-detail', storage_id=storage.id)
    
    return render(request, 'homepage/remove_storage_item.html', {
        'storage_item': storage_item,
        'storage': storage
    })

def logistics_timeline(request, Tag_number):
    """物流时间线可视化"""
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    tracking_records = LogisticsTracking.objects.filter(livestock=livestock).order_by('timestamp')
    
    # 准备时间线数据
    timeline_data = []
    for record in tracking_records:
        timeline_data.append({
            'time': record.timestamp.strftime('%Y-%m-%d %H:%M'),
            'status': record.get_status_display(),
            'location': record.location,
            'location_type': record.get_location_type_display(),
            'temperature': record.temperature,
            'humidity': record.humidity,
            'operator': record.operator.username if record.operator else '系统',
            'notes': record.operation_notes
        })
    
    return render(request, 'homepage/logistics_timeline.html', {
        'livestock': livestock,
        'timeline_data': timeline_data,
        'has_records': len(timeline_data) > 0
    })

def show_logistics_list(request):
    """显示物流追踪列表"""
    if not request.user.is_authenticated:
        return redirect('authentication:login')
    
    # 获取所有物流追踪记录，按时间倒序排列
    logistics_list = LogisticsTracking.objects.filter(user=request.user).order_by('-timestamp')
    
    # 统计信息
    total_count = logistics_list.count()
    shipped_count = logistics_list.filter(status='shipped').count()
    delivered_count = logistics_list.filter(status='delivered').count()
    
    # 今日新增
    today = timezone.now().date()
    today_count = logistics_list.filter(timestamp__date=today).count()
    
    # 筛选功能
    status_filter = request.GET.get('status')
    batch_id_filter = request.GET.get('batch_id')
    date_from_filter = request.GET.get('date_from')
    date_to_filter = request.GET.get('date_to')
    
    if status_filter:
        logistics_list = logistics_list.filter(status=status_filter)
    
    if batch_id_filter:
        logistics_list = logistics_list.filter(livestock__Tag_number__icontains=batch_id_filter)
    
    if date_from_filter:
        logistics_list = logistics_list.filter(timestamp__date__gte=date_from_filter)
    
    if date_to_filter:
        logistics_list = logistics_list.filter(timestamp__date__lte=date_to_filter)
    
    return render(request, 'homepage/show_logistics_list.html', {
        'logistics_list': logistics_list,
        'total_count': total_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'today_count': today_count,
        'status_filter': status_filter or '',
        'batch_id_filter': batch_id_filter or '',
        'date_from_filter': date_from_filter or '',
        'date_to_filter': date_to_filter or ''
    })
