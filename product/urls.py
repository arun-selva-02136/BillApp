from django.urls import path
from .views import( HomePage, SignupPage, LogoutPage,LoginPage,vendor_list,vendor_form,product_list,
                   category_list, category_detail, category_create, category_edit, category_delete,
                    product_list,product_form,product_detail,sales_list,product_edit,product_delete,
                    category_generate_excel,product_generate_excel,product_generate_pdf,get_related_products,my_view,bill_manage,handle_modified_data,resources,profile
                    ,category_delete_multiple,product_delete_multiple,category_generate_pdf,customer,sales_get_data)
from django.conf import settings
from django.conf.urls.static import static
# yourapp/urls.py
from django.urls import path
from .views import show_data, input_customer



urlpatterns = [
    path('', LoginPage, name='login'),
    path('signup/', SignupPage, name='signup'),    
    path('logout/', LogoutPage, name='logout'),
    path('my_view/',my_view,name='my_view'),
    path('home/', HomePage, name='home'),
    path('profile/', profile, name='profile'),
    
    path('vendors/', vendor_form, name='vendor_form'),
    path('vendors/lists/', vendor_list, name='vendor_list'),
    # path('vendors/<int:vendor_id>/', vendor_form, name='vendor_form'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', category_delete, name='category_delete'),
# urls.py
    path('categories/delete/multiple/', category_delete_multiple, name='category_delete_multiple'),
    path('products/delete/multiple/', product_delete_multiple, name='product_delete_multiple'),
    path('sales/data/', sales_get_data, name='sales_get_data'),

    path('products/', product_list, name='product_list'),
    path('products/create', product_form, name='product_create'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', product_delete, name='product_delete'),
    # path('404',handler404,name='404'),
    path('sales/', sales_list, name='sales_list'),
    # path('sales/add/', add_sales, name='add_sales'),
    # path('products/create/', product_create, name='product_create'),
    path('product_generate_excel/', product_generate_excel, name='product_generate_excel'),
    path('category_generate_excel/', category_generate_excel, name='category_generate_excel'),
    path('product_generate_pdf/', product_generate_pdf, name='product_generate_pdf'),
    path('category_generate_pdf/', category_generate_pdf, name='category_generate_pdf'),
    # path('plotview/', plot_view, name='plot_view'),
    path('show_data/', show_data, name='show_data'),
    path('input_customer/', input_customer, name='input_customer'),
    path('get_related_products/', get_related_products, name='get_related_products'),
    path('bill_manage/', bill_manage, name='bill_manage'),
    path('handle-modified-data/', handle_modified_data, name='handle_modified_data'),
    path('iframe/', resources, name='iframe'),
    path('customer/', customer, name='customer'),
    # path('input_sales/', input_sales, name='input_sales'),



    # path('search/', search_view, name='search'),

    

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
