from django import forms
from .models import Account,Category,Vendor,Sales,Product ,Customer  
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = ['username', 'password']
# class AccountForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ['username', 'password', 'phone_num', 'role']

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['category_name', 'category_code',]

# class VendorForm(forms.ModelForm):
#     class Meta:
#         model = Vendor
#         fields = ['name', 'phone_num', 'gst_num', 'invoice_num', 'address','vendor_id']

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'category', 'brand', 'mrp', 'price', 'unit', 'qty', ]

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['category_name', 'category_code', 'category_descriptions', 'category_created', 'category_image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['category_created']
        # Ensure that 'category_image' is not mentioned here with required=False
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Purchase
#         fields = '__all__'
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'



################################################################################
# class SalesForm(forms.ModelForm):
#     class Meta:
#         model = Sales
#         fields = '__all__'

# # forms.py


# SalesFormSet = formset_factory(SalesForm, extra=3)  # Set extra to the number of rows you want to display initially
###############################################################################

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'
# class Sales_ProductsForm(forms.ModelForm):
#     class Meta:
#         model = Sales_Products 
#         fields = '__all__'
