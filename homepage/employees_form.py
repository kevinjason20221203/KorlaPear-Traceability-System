from django import forms
from .models import Employees


class EmployeesForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = [
            "Eid",
            "Name",
            "Country_code",
            "Phone_number",
            "Position",
            "Salary",
            "Performance",
        ]
        labels = {
            "Eid": "员工编号",
            "Name": "姓名",
            "Country_code": "国家代码",
            "Phone_number": "电话号码",
            "Position": "工作岗位",
            "Salary": "工资数额",
            "Performance": "工作表现",
        }
