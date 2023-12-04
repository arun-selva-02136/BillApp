# from django.contrib import admin
# from .models import Register,Vendor,Product,Account
# # Register your models here.
# admin.site.register(Register)
# admin.site.register(Vendor)
# admin.site.register(Product)
# admin.site.register(Account)
from django.contrib import admin
from .models import Account,Category,Vendor,Customer,Sales,Product,Purchase,Sales_Products
from django.contrib.auth.models import Group,User

# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('admin_id', 'username', 'phone_num', 'role')
#     search_fields = ('username', 'phone_num','role',)

class AccountAdmin(admin.ModelAdmin):
    # list_display = ( 'username', 'password', 'phone_num', 'role','Account_date')
        list_display = [field.name for field in Account._meta.get_fields()]

admin.site.register(Account,AccountAdmin)
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('category_id', 'name', 'category_code')
#     search_fields = ('name', 'category_code','category_id')
admin.site.register(Category)

# @admin.register(Vendor)
# class VendorAdmin(admin.ModelAdmin):
#     list_display = ('vendor_id', 'name', 'phone_num', 'gst_num', 'invoice_num', 'address')
#     search_fields = ('name', 'phone_num', 'gst_num','vendor_id',)
admin.site.register(Vendor)
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('purchases_id', 'product_name', 'category_name', 'brand', 'mrp', 'price', 'unit', 'qty','purchase_created' ,'purchase_modified')
#     search_fields = ('name', 'category__name', 'brand', 'vendor__name','purchases_id')
# admin.site.register(Purchases)

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('customer_name', 'customer_id', 'phone_num',)
#     search_fields = ('customer_name','customer_id' )
admin.site.register(Customer)

# class SalesAdmin(admin.ModelAdmin):
#     list_display = ( 'customer_id', 'purchases_id',)
#     search_fields = ('purchases_id','customer_id','sales_id' )
admin.site.register(Sales)
admin.site.register(Purchase)
# admin.site.register(Product)
class  ProductAdmin(admin.ModelAdmin):
    # list_display = ( 'supplier', 'product','quantity','unit_price','total_amount'),'purchase_date'
    search_fields = ('supplier','product','quantity','unit_price','total_amount' ,'purchase_date')
admin.site.register(Product,ProductAdmin)
admin.site.register(Sales_Products)
