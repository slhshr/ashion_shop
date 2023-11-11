from django.forms import ModelForm
from django import forms
from .models import *


class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'







