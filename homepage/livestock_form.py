from django import forms 
from .models import Livestock, Livestock_production,Milk_production,Eggs_production

class LivestockForm(forms.ModelForm):
    class Meta:
        model= Livestock
        fields=[
            'Tag_number',
            'Animal_type',
            'Age',
            'Breed',
        ]
        labels = {
            'Tag_number': '批次号',
            'Animal_type': '物流类型',
            'Age': '存储时长(天)',
            'Breed': '产品规格',
        }

class Livestock_productionForm(forms.ModelForm):
    class Meta:
        model=Livestock_production
        fields=[
            'Production_date',
            'Production_amount',
            'Feed_consumed',
            'Comments'
        ]
        labels = {
            'Production_date': '生产日期',
            'Production_amount': '生产数量',
            'Feed_consumed': '饲料消耗(kg)',
            'Comments': '备注',
        }

class Milk_productionForm(forms.ModelForm):
    class Meta:
        model=Milk_production
        fields=[
            'Year',
            'Month',
            'Day',
            'Livestock_number',
            'Morning_production',
            'Midday_production',
            'Evening_production',
            'Morning_consumption',
            'Evening_consumption'
        ]
        labels = {
            'Year': '年份',
            'Month': '月份',
            'Day': '日期',
            'Livestock_number': '作业数量/规模',
            'Morning_production': '上午产出',
            'Midday_production': '中午产出',
            'Evening_production': '晚上产出',
            'Morning_consumption': '上午消耗',
            'Evening_consumption': '晚上消耗',
        }

class Egg_productionForm(forms.ModelForm):
    class Meta:
        model=Eggs_production
        fields=[
            'Year',
            'Month',
            'Day',
            'Poultry_number',
            'Morning_egg_collection',
            'Midday_egg_collection',
            'Evening_egg_collection',
            'Morning_feeds',
            'Evening_feeds',
            'Comments'
        ]
        labels = {
            'Year': '年份',
            'Month': '月份',
            'Day': '日期',
            'Poultry_number': '家禽数量',
            'Morning_egg_collection': '早晨收集',
            'Midday_egg_collection': '中午收集',
            'Evening_egg_collection': '晚上收集',
            'Morning_feeds': '早晨饲料(kg)',
            'Evening_feeds': '晚上饲料(kg)',
            'Comments': '备注',
        }
