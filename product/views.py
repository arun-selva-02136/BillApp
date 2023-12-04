from django.shortcuts import render, HttpResponse, redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from .models import  Category,Vendor,Account,Customer,Sales,Product,Purchase,Sales_Product
# from django.contrib import messages
from django.db import connection
# from django.db.models import Q
from django.db import models
from .forms import CategoryForm,SalesForm,CustomerForm
from django.contrib.auth.hashers import check_password,make_password
# from django.urls import reverse
from datetime import datetime
from django.http import HttpResponse
# from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
# from billing_system import settings
import pandas as pd
import csv

from decimal import Decimal

from functools import wraps
from django.shortcuts import redirect


############################ login_required and admin_required ########################################

def resources(request):
    return render(request,'iframe/Iframe.html')


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Implement your custom authentication logic
        if 'user_data' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to your login page or some unauthorized page
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Implement your custom admin role check
        if 'user_data' in request.session and request.session['user_data'].get('role') == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to your login page or some unauthorized page
    return wrapper
############################ TOTAL AMOUNT CALCULATION  ########################################

def total_amount(quantity,price):
    return quantity * price
############################ ADMIN ########################################
def HomePage(request,):
    resources(request)
    user_data = request.session.get('user_data')
    with connection.cursor() as cursor:
            cursor.execute("SELECT role FROM product_account WHERE username=%s AND admin_id=%s ", [user_data['username'],user_data['admin_id']])
            role = cursor.fetchone()
    total_quantity = Product.objects.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    # print(total_quantity)
    purchases = Product.objects.all()
    products_purchase= Purchase.objects.all()
    # Calculate the total amount for all purchases
    total_amount = sum([purchase.total_amount for purchase in purchases])
    print(total_amount)
    total_purcheas_amount =sum([purchase.total_amount for purchase in products_purchase])
    print(total_purcheas_amount)
    data={'user':user_data['username']}
    print(data)
    context ={
    'available_total_quantity':total_quantity,
    'available_purchases_amount':total_amount,
    'purchase_amount': total_purcheas_amount,
    'role':role[0] ,        
    'user':user_data['username'],
    'account' :len(Account.objects.all()),
    'customer':  len(Customer.objects.all())}

    context['sales'] = len(Sales.objects.all())
    context['category'] = len(Category.objects.all())
    context['vendor'] = len(Vendor.objects.all( ))
    
    product_tot = Product.objects.all()
    pro_amount = [pro.total_amount for pro in product_tot]
    print("product_total : ", pro_amount)
    context['pro_val'] = [float(str(provalue)) for provalue in pro_amount]
    
    sale_total = Sales_Product.objects.all()
    sales_list_val = [sale.total_amount for sale in sale_total]
    print(sales_list_val)
            
    # Extract numeric values without Decimal('')
    context['nume_val'] = [float(str(value)) for value in sales_list_val]
    return render(request, 'home.html',context=context)


############################ LOGIN ########################################
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        phone_num = request.POST.get('phone_num')
        role = request.POST.get('role')
        hashed_pass = make_password(pass1)


        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            account_obj = Account(username=uname, email=email, password=hashed_pass,phone_num=phone_num,role=role)
            account_obj.save()
          
            return redirect('login')

    return render(request, 'signup.html')



def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        with connection.cursor() as cursor:
            cursor.execute("SELECT admin_id, role,username, password FROM product_account WHERE username=%s   ", [username,])
            user_data = cursor.fetchone()
        print(user_data)
        if user_data is None:
            context = {'data_error': "No username. Can you register now?"}
            print(context)
            return render(request, 'login.html', context=context)
        else:
            admin_id,role, fetched_username, hashed_password = user_data
            if check_password(password, hashed_password):
                request.session['user_data'] = {'admin_id': admin_id, 'username': fetched_username,'role':role}
                return redirect('iframe')
            else:
                context = {'data_error': "Incorrect password"}
                return render(request, 'login.html', context=context)

    return render(request, 'login.html')


def profile(request):
    return render(request,'profile.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


############################ CATEGORIES  ########################################
# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'category_list.html', {'categories': categories})

def category_list(request):
    categories_with_qty = []

    # Fetch all categories
    categories = Category.objects.all()

    # Loop through each category and fetch relevant information
    for category in categories:
        # Fetch the total quantity available for the category from the Product table
        total_qty = Product.objects.filter(category_name=category).aggregate(models.Sum('quantity')).get('quantity__sum') or 0
        print(total_qty)
        # Create a dictionary with relevant information
        category_info = {
            'category': category,
            'category_image':category.category_image,
            'category_code': category.category_code,
            'category_descriptions': category.category_description,
            'available_quantity': total_qty or 0,
            # 'length':len(total_qty)
        }

        # Append the dictionary to the list
        categories_with_qty.append(category_info)
        print(categories_with_qty)

    return render(request, 'category_list.html', {'categories_with_qty': categories_with_qty,'length':len(categories_with_qty)})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'category_detail.html', {'category': category})




# def category_create(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm()
#     return render(request, 'category_form.html', {'form': form})

def category_create(request):
        
        if request.method == 'POST':
            print('hai')
            category_name=request.POST.get('category_name')
            print(category_name)
            category_code = request.POST.get('category_code')
            print(category_code)
            category_description = request.POST.get('category_description')
            print(category_description)
            category_created = datetime.now()
            category_image = request.FILES.get('category_image', None)
            print(category_image)
            new_category = Category(
                category_name=category_name,
                category_code=category_code,
                category_description=category_description,
                category_created=category_created,
                category_image=category_image
             )
            new_category.save()
            return redirect('category_list')

        return render(request, 'category_form.html', )



# def category_edit(request, category_id):
#     print(category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     print(category.category_description)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         context={
#             'category':category,
#             'edit_mode':True,
#         }
#     return render(request, 'category_form.html',context=context)
def category_edit(request, category_id):
    # Retrieve the category object
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        # Update category attributes based on form data
        category.category_name = request.POST.get('category_name', '')
        category.category_description = request.POST.get('category_description', '')
        category.category_code = request.POST.get('category_code', '')
        if 'category_image' in request.FILES:
            category.category_image = request.FILES['category_image']
        print(category.category_image)
        # Save the updated category
        category.save()
        
        # Redirect to the category list view
        return redirect('category_list')

    # Render the edit category form
    context = {
        'category': category,
        'edit_mode':True,

    }
    return render(request, 'category_form.html', context)
# views.py
# from django.http import JsonResponse

# def category_delete_multiple(request):
#     print('hai')
#     if request.method == 'POST':
#         try:
#             print('.........')
#             data = json.loads(request.body)
#             print(data)
#             category_ids = data.get('Category_id', [])
#             Category.objects.filter(id__in=category_ids).delete()
#             return JsonResponse({'message': 'Categories deleted successfully'})
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# views.py
from django.http import JsonResponse

def category_delete_multiple(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            category_ids = [item['Category_id'] for item in data.get('category_ids', [])]

            # Check if category_ids is not empty before deleting
            if category_ids:
                # Category.objects.filter(id__in=category_ids).delete()
                Category.objects.filter(category_id__in=category_ids).delete()

                return JsonResponse({'message': 'Categories deleted successfully'})
            else:
                return JsonResponse({'error': 'No category IDs provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def category_delete(request, category_id):
    
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

############################ PRODUCT VENDOR ########################################

def vendor_list(request,vendor_id=None):

    vendor_list = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendor_list': vendor_list})

# iframe/add
def vendor_form(request, vendor_id=None):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id) if vendor_id else None

    if request.method == 'POST':
        # Assuming you have form data in the request.POST dictionary
        name = request.POST.get('name')
        phone_num = request.POST.get('phone_num')
        gst_num = request.POST.get('gst_num')
        invoice_num = request.POST.get('invoice_num')
        address = request.POST.get('address')

        vendor= Vendor.objects.create(
                vendor_name=name,
                phone_num=phone_num,
                gst_num=gst_num,
                invoice_num=invoice_num,
                address=address
            )
        vendor.save()

        return redirect('vendor_list')  # Change 'vendor_list' to the appropriate URL name

    return render(request, 'vendor_form.html', {'vendor': vendor})
############################ PRODUCT OR PURECHAES ########################################
#  path('products/', product_list, name='product_list'),
#     path('products/create', product_form, name='product_create'),
#     path('products/<int:purchases_id>/', product_detail, name='product_detail'),
#     path('products/<int:purchases_id>/edit/', product_edit, name='product_edit'),
#     path('products/<int:purchases_id>/delete/', product_delete, name='product_delete'),


def product_form(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    print('hai')
    demo =[('active', 'Active'), ('disabled', 'Disabled')]
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_name = request.POST.get('category_name')
        sub_category = request.POST.get('sub_category' or None) 
        sku = request.POST.get('sku'or None) 
        hsn_code = request.POST.get('hsn_code'or None) 
        description = request.POST.get('description'or None) 
        brand = request.POST.get('brand' or None)
        mrp = float(request.POST.get('mrp') or 0)
        price = float(request.POST.get('price'))
        unit = request.POST.get('unit') or None
        quantity = float(request.POST.get('quantity'))
        vendor_id = request.POST.get('vendor_id')
        purchase_modified = request.POST.get('purchase_modified')
        gst = request.POST.get('tax') or '1%'
        discount = request.POST.get('discount') or '1%' 
        status = request.POST.get('status' ) or 'Active'
        print()

        amount=total_amount(float(quantity),float(price))
        print(f'this is qty+{quantity}')
        print(f'this is price+{price}')
        print(f'this is amount{type(amount)}')
        # total_amount=amount
        # Handle product_images file upload
        product_image = request.FILES.get('product_image'or None)
        
        purchase_created = datetime.now()

        # Get or create the Category instance
        category_instance, created_category = Category.objects.get_or_create(category_name=category_name)

        # Get or create the Vendor instance
        vendor_instance, created_vendor = Vendor.objects.get_or_create(vendor_id=vendor_id)

        # Check if the Product with the given attributes already exists
        existing_product = Product.objects.filter(
            products_name=product_name,
            category_name=category_instance,
            brand=brand,
            mrp=mrp,
            price=price,
            unit=unit,
            vendor_id=vendor_instance
        ).first()
        print(existing_product)
        if existing_product:
            # Update the existing Product instance
            existing_product.quantity += int(quantity)
            existing_product.total_amount += amount
            existing_product.save()

            # Create a new Purchase instance
            new_purchase = Purchase(
                product_name=existing_product,
                category_name=category_instance,
                sub_category = sub_category,

                brand=brand,
                mrp=mrp,
                price=price,
                unit=unit,
                quantity=quantity,
                vendor_id=vendor_instance,
                purchase_created=purchase_created,
                gst=gst,
                discount=discount,
                status=status,
                product_image=product_image,
                total_amount = amount,
                description = description,
                hsn_code = hsn_code,
                sku = sku,
                    
                
            )
            new_purchase.save()
        else:
            # Create a new Product instance
            new_product = Product(
                products_name=product_name,
                category_name=category_instance,
                sub_category = sub_category,

                brand=brand,
                mrp=mrp,
                price=price,
                unit=unit,
                quantity=quantity,
                vendor_id=vendor_instance,
                product_modified=purchase_modified,
                product_created=purchase_created,
                gst=gst,
                discount=discount,
                status=status,
                product_image=product_image,
                total_amount = amount,
                description = description,
                hsn_code = hsn_code,
                sku = sku,
                    
            )
            new_product.save()

            # Create a new Purchase instance
            new_purchase = Purchase(
                product_name=product_name,
                category_name=category_instance,
                sub_category = sub_category,

                brand=brand,
                mrp=mrp,
                price=price,
                unit=unit,
                quantity=quantity,
                vendor_id=vendor_instance,
                purchase_created=purchase_created,
                gst=gst,
                discount=discount,
                status=status,
                product_image=product_image,
                total_amount = amount,
                description = description,
                hsn_code = hsn_code,
                sku = sku,
                    

            )
            new_purchase.save()

        return redirect('product_list')
    
    context = {
        'categories': categories,
        'vendors': vendors,
        'status': demo,}  # Include status choices in the context

    return render(request, 'product_form.html', context=context)


def product_list(request):
    products = Product.objects.all()
    
    return render(request, 'product_list.html', {'products': products,'length':len(products)})


def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def product_edit(request, product_id):# ... other form fields
    product = get_object_or_404(Product, product_id=product_id)
    print(product.product_id)
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    demo =[('active', 'Active'),  ('disabled', 'Disabled')]

    if request.method == 'POST':

        # Handle form submission if needed
        product.products_name = request.POST.get('product_name')
        category_name = request.POST.get('category_name')
        category, created = Category.objects.get_or_create(category_name=category_name)
        product.category_name = category
        product.sub_category = request.POST.get('sub_category'or None) 
        print(product.sub_category)
        vendor_id = request.POST.get('vendor_id')
        product.sku = request.POST.get('sku' or None )
        product.hsn_code = request.POST.get('hsn_code' or None) 
        product.description = request.POST.get('description' or None) 
        print(product.sku)
        print(product.hsn_code)
        print(product.description)
        vendor, created_vendor = Vendor.objects.get_or_create(vendor_id=vendor_id)
        product.vendor_id = vendor
        product.brand = request.POST.get('brand' or None)
        print(product.brand)
        product.mrp = float(request.POST.get('mrp') or 0)
        print(product.mrp,'1')
        product.price = float(request.POST.get('price'))
        print(product.price,'2')
        product.unit = request.POST.get('unit') or None
        print(product.unit,'3')
        product.quantity = float(request.POST.get('quantity'))
        print(product.quantity,'4')
        product.purchase_created = datetime.now()
        date2= datetime.now()
        print(product.product_created)
        product.tax = request.POST.get('tax') or '1%'
        print(product.tax)
        product.discount = request.POST.get('discount') or '1%'
        print(product.discount)
        product.status = request.POST.get('status') or 'Active'
        print(product.status)
        # print(print.status)

        amount=total_amount(product.quantity,product.price)
        print(amount)
        product.total_amount=amount
        
        product.product_image = request.FILES.get('product_image'or None)
        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']
            product.save()
        print('...............')
        print(product.product_image)
        # Check if a product with the same attributes already exists
        existing_product = Product.objects.filter(
            products_name=product.products_name,
            category_name=product.category_name,
            brand=product.brand,
            mrp=product.mrp,
            price=product.price,
            unit=product.unit,
            vendor_id=product.vendor_id
        ).first()
        if existing_product and existing_product.unit != product.unit:
    # Create a new product because the unit is different
            existing_product = None   
        print(product.unit) 
        print('------------------------')  
        if existing_product:
            # Update the existing Product instance
            existing_product.quantity += (product.quantity)
            existing_product.total_amount += product.total_amount
            existing_product.status = product.status
            existing_product.product_modified=product.product_created
            existing_product.save()

            # Update the corresponding Purchase entry

                # If somehow there is no corresponding Purchase entry, create a new one
            new_purchase = Purchase(
                    product_name=existing_product.products_name,
                    category_name=existing_product.category_name,
                    sub_category = product.sub_category,
                    brand=existing_product.brand,
                    mrp=existing_product.mrp,
                    price=existing_product.price,
                    unit=existing_product.unit,
                    quantity=existing_product.quantity,
                    vendor_id=existing_product.vendor_id,
                    purchase_created=product.purchase_created ,
                    gst=product.gst,
                    discount=product.discount,
                    status=product.status,
                    product_image=product.product_image,
                    total_amount = product.total_amount,
                    description = product.description,
                    hsn_code = product.hsn_code,
                    sku = product.sku,
                    

                    
                )
            new_purchase.save()

        else:
            # Create a new Product instance
            new_product = Product(
                products_name=product.products_name,
                category_name=product.category_name,
                sub_category = product.sub_category,
                brand=product.brand,
                mrp=product.mrp,
                price=product.price,
                unit=product.unit,
                quantity=product.quantity,
                vendor_id=product.vendor_id,
                product_created=product.purchase_created,
                gst=product.gst,
                discount=product.discount,
                status=product.status,
                product_image=product.product_image,
                total_amount = product.total_amount,
                description = product.description,
                hsn_code = product.hsn_code,
                sku = product.sku
            )
            new_product.save()

            # Create a new Purchase entry
            new_purchase = Purchase(
                product_name=product.products_name,
                category_name=product.category_name,
                sub_category = product.sub_category,
                brand=product.brand,
                mrp=product.mrp,
                price=product.price,
                unit=product.unit,
                quantity=product.quantity,
                vendor_id=product.vendor_id,
                purchase_created=date2,
                gst=product.gst,
                discount=product.discount,
                status=product.status,
                product_image=product.product_image,
                total_amount = product.total_amount,
                description = product.description,
                hsn_code = product.hsn_code,
                sku = product.sku
            )
            new_purchase.save()

        return redirect('product_list')

    else:
        # Provide the existing data to the HTML template
        context = {
            'product': product,
            'categories': categories,
            'vendors': vendors,
            'status': demo,

            'edit_mode': True,
            'form': {
                'product_name': product.products_name,
                'category_name': product.category_name.category_name if product.category_name else '',
                'brand': product.brand,
                'sub_category': product.sub_category,
                'mrp': product.mrp,
                'price': product.price,
                'unit': product.unit,
                'quantity': product.quantity,
                'vendor_id': product.vendor_id.vendor_id if product.vendor_id else '',
                'description' : product.description,
                'hsn_code' :product.hsn_code,
                'sku': product.sku,
                'status': product.status,
                'gst' :product.gst,
                'discount': product.discount,
                'product_image': product.product_image,
                
            }
        }

    return render(request, 'product_form.html', context=context)



def product_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')


    return render(request, 'product_confirm_delete.html', {'product': product})



def product_delete_multiple(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            product_ids = [item['product_id'] for item in data.get('product_ids', [])]
            print(product_ids)
            # Check if category_ids is not empty before deleting
            if product_ids:
                # Category.objects.filter(id__in=category_ids).delete()
                Product.objects.filter(product_id__in=product_ids).delete()

                return JsonResponse({'message': 'Products deleted successfully'})
            else:
                return JsonResponse({'error': 'No product IDs provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


###################### SEARCH ###################################

# def search(request):
#     query=None
#     results=[]
#     if request.method=="GET":
#         query=request.GET.get('search')
#         results=Category.objects.filter(Q(customer_name__icontains=query)  )
#         # results=Category.objects.filter(Q(customer_name__icontains=query) | Q(body__icontains=query) | Q(footer__icontains=query) )
#     return  render(request,'.html',{'query': query,
#                                           'results': results})
###################### PDF AND EXCEL ###################################


####################### TYPE 1 PDF 5 ROWS  ###########################
# def generate_pdf(request):
#     # Fetch data from the database
#     products_query = Product.objects.values()
#     df = pd.DataFrame.from_records(products_query)

#     # Number of columns per group
#     columns_per_group = 5

#     # Split columns into groups
#     column_groups = [df.columns[i:i + columns_per_group] for i in range(0, len(df.columns), columns_per_group)]

#     # Create PDF document in memory
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)

#     # List to hold tables
#     tables = []

#     # Loop through column groups
#     for group in column_groups:
#         # Extract relevant columns
#         group_df = df[group]

#         # Convert the group DataFrame to a list of lists
#         data = [group_df.columns.tolist()] + group_df.values.tolist()

#         # Create a table
#         table = Table(data)

#         # Style the table
#         style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                             ('GRID', (0, 0), (-1, -1), 1, colors.black)])

#         table.setStyle(style)

#         # Add the table to the list
#         tables.append(table)

#         # Add space between groups
#         tables.append(Table([[None]] * 3))  # 3 rows of None for space

#     # Build the PDF document
#     doc.build(tables)

#     # Rewind the buffer and create a response
#     buffer.seek(0)
#     response = HttpResponse(buffer.read(), content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="output.pdf"'

#     return response

def product_generate_excel(request):
    # Fetch available product lists (you can customize this query based on your needs)
    # products = Product.objects.filter(status='active')
 if request.method == 'POST' or 'GET':
   # views.py
    model_fields = Product._meta.get_fields()
    column_names = [field.name for field in model_fields if field.name != 'id']  # Exclude 'id' field

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product__data.csv"'

    writer = csv.writer(response)
    writer.writerow(column_names)

    # Replace YourModel.objects.all() with your actual query to retrieve data from MySQL
    queryset = Product.objects.all()

    for row in queryset:
        row_data = [getattr(row, field) for field in column_names]
        writer.writerow(row_data)

    return response
 else:
     print('bye')


def category_generate_excel(request):
    # Fetch available product lists (you can customize this query based on your needs)
    # products = Product.objects.filter(status='active')
 if request.method == 'POST' or 'GET':
   # views.py
    model_fields = Category._meta.get_fields()
    column_names = [field.name for field in model_fields[2:] if field.name != 'id']  # Exclude 'id' field

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="category_data.csv"'

    writer = csv.writer(response)
    writer.writerow(column_names)

    # Replace YourModel.objects.all() with your actual query to retrieve data from MySQL
    queryset = Category.objects.all()

    for row in queryset:
        row_data = [getattr(row, field) for field in column_names]
        writer.writerow(row_data)

    return response
 else:
     print('bye')
#########################     ready of   pdf   #########################################

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Product  # Import your Product model

def product_generate_pdf(request):
    products = Product.objects.all()  # Change to your model name
    template_path = 'product_pdf.html'
    

    total_purcheas_amount =sum([purchase.total_amount for purchase in products])

    context = {'products': products,'total_purcheas_amount':total_purcheas_amount}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_list.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def category_generate_pdf(request):
    products = Product.objects.all()  # Change to your model name
    template_path = 'product_pdf.html'
    

    total_purcheas_amount =sum([purchase.total_amount for purchase in products])

    context = {'products': products,'total_purcheas_amount':total_purcheas_amount}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="category_list.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



###################### SALES ###################################
def sales_list(request):
    sales_data = Sales.objects.all()
    return render(request, 'sales_list.html', {'sales_data': sales_data})

def show_data(request):
    customers = Customer.objects.all()
    sales = Sales.objects.all()
    return render(request, 'show_data.html', {'customers': customers, 'sales': sales})

def input_customer(request):
    product_lists=Product.objects.all()
    product_lists = [
        {'Product ID': product.product_id, 'name': product.products_name,'hns':product.hsn_code,'qty':product.qty, 'sgstNo': product.tax, 'cgst' : product.tax , 'amount': product.price,'discount':product.discount,}
        for product in product_lists]
    print(product_lists)
    if request.method == 'POST':
      pass    
    return render(request, 'bill_manage.html', {'sales': product_lists})


####################################  STATUS PAGES ####################################################
def page_not_found(request, exception):
    return render(request, '404.html', status=404)
def server_error(request):
    return render(request, '500.html', status=500)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

@csrf_exempt
def get_related_products(request):
    if request.method == 'POST':
        try:
            # Get the product name from the request body
            data = json.loads(request.body)
            product_name = data.get('product_name', '')

            # Query the database for related products
            related_products = Product.objects.filter(product_name__icontains=product_name)

            # Convert the product data to a JSON response
            data = [{'product_name': product.product_name, 'description': product.description, 'price': str(product.price)} for product in related_products]
            return JsonResponse(data, safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)

    return JsonResponse({'error': 'GET method not allowed'}, status=405)
#########################################################################################
# views.py















###################################   sales row demos      ############################################################
from django.shortcuts import render

def my_view(request):
    product_lists=Product.objects.all()
    # product_lists = [[product.product_id, product.products_name, product.price] for product in product_lists]

    product_lists = [
        {'Product ID': product.product_id, 'Product Name': product.products_name, 'Price': product.price,'Hsn_code':product.hsn_code,'Tax':product.tax}
        for product in product_lists]
    print(product_lists)
        # return render(request, 'my_templates.html', {'my_data': my_data})
    return render(request, 'my_templates.html', {'product_lists': product_lists})




from django.shortcuts import render
from django.http import JsonResponse

def bill_manage(request):
    product= Product.objects.all()
    
    customers = Customer.objects.all()
    customer_lists=[{'name':customer.customer_name,'number':customer.customer_number,'id':customer.customer_id} for customer in customers ]
    product_lists = [
        {'product_id': product.product_id, 'name': product.products_name,'qty':product.quantity, 'amount': product.price,'hns':product.hsn_code,'sgstNo':product.gst ,  'cgst':product.gst,'discount':product.discount}
        for product in product]
    # print(product_lists)
    # data_to_modify = [["item1", "item2", "item3"],["item1", "item2", "item3"]]
    return render(request, 'demoss.html', {'data_to_modify': 'data_to_modify','products':product_lists,'customers':customer_lists})


import json
from django.http import JsonResponse

def handle_modified_data(request):
    if request.method == 'POST':
        modified_data_json = request.POST.get('modified_data')
        
        try:
            modified_data = json.loads(modified_data_json)
                        
            return JsonResponse({'message': 'Data received successfully!', 'modified_data': modified_data})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format.'}, status=400)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)




def customer(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_number = request.POST.get('customer_number')
        customer_created= datetime.now()
        customer_obj = Customer(customer_name=customer_name, customer_number=customer_number, customer_created=customer_created)
        customer_obj.save()
        return redirect('bill_manage')  # Redirect to your login page or some unauthorized page

###########################################################333333
# def sales_get_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print('----------------------------------------------------')
#             print(data)
#             product_ids = [item for item in data.get('product_ids', [])]
#             product = [item for item in data.get('tables', [])]
            
#             print(product_ids)
#             print('###################################################3')

#             print(product)
#             print('###################################################3')

#             # Check if category_ids is not empty before deleting
#             if product_ids:
#                 # Category.objects.filter(id__in=category_ids).delete()
#                 Product.objects.filter(product_id__in=product_ids).delete()

#                 return JsonResponse({'message': 'Products deleted successfully'})
#             else:
#                 return JsonResponse({'error': 'No product IDs provided'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)




# from django.http import JsonResponse
# import json
# from .models import Product, Sales_Product

# def sales_get_data(request):
#     if request.method == 'POST':
#             data = json.loads(request.body)
#             # print(data)
#             product_ids = [item for item in data.get('product_ids', [])]
#             sales_product_ids = [item for item in data.get('tables', [])]

#             # print(product_ids)
#             # print(sales_product_ids)

           
#             for sales_product_id in sales_product_ids:
#                 print(sales_product_id)
#                 return JsonResponse({'error': 'Invalid request method'}, status=400)
#     #                 try:
#     #                     # sales_product = Sales_Product.objects.get(sales_products_id=sales_product_id)
#     #                     product = Product.objects.get(products_name=sales_product.product_name)
#     #                     product.qty -= sales_product.quantity
#     #                     product.save()
#     #                 except (Sales_Product.DoesNotExist, Product.DoesNotExist):
#     #                     return JsonResponse({'error': 'Sales_Product or Product does not exist'}, status=400)

#     #                 return JsonResponse({'message': 'Products and Sales_Product entries deleted successfully'})
#     #         else:
#     #             return JsonResponse({'error': 'No product IDs provided'}, status=400)
#     #     except json.JSONDecodeError:
#     #         return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)
###########################################################3
# from django.http import JsonResponse
# import json
# from .models import Sales

# def sales_get_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # print(data)
#             sales_product_ids = [item for item in data.get('tables', [])]
#             print(sales_product_ids)
#             print(sales_product_ids['productName'])
#             for sales_product_id in sales_product_ids:
#                 # print(sales_product_id.get('quantity'),)
#                 print(sales_product_id['productName'])
#                 # Assuming you have the necessary fields in your data dictionary
#                 # sales_data = {

#                     # 'customer_name': sales_product_id.get('customer_name'),
#                     # 'customer_phone_number': data.get('customer_phone_number'),
#                     # 'number_of_products': sales_product_id.get('number_of_products'),
#                     # 'quantity': sales_product_id.get('quantity'),
#                     # 'sgst_no': data.get('sgst_no'),
#                     # 'cgst_no': data.get('cgst_no'),
#                     # 'actual_amount': data.get('actual_amount'),
#                     # 'discount_amount': data.get('discount_amount'),
#                     # 'net_amount': data.get('net_amount'),
#                     # 'customer_giving_amount': data.get('customer_giving_amount'),
#                     # 'balance_given_amount': data.get('balance_given_amount'),
#                     # 'sale_datetime': data.get('sale_datetime'),
#                     # 'payment_type': data.get('payment_type'),
#                     # 'bill_no': data.get('bill_no'),
#                     # 'gst_no': data.get('gst_no'),
#                 # }

#                 # Create a new Sales instance and save it
#                 # sales_instance = Sales(**sales_data)
#                 # sales_instance.save()

#             return JsonResponse({'message': 'Sales data saved successfully'})
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)


def sales_get_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sales_product_ids = [item for item in data.get('tables', [])]
            product_ids = [item for item in data.get('product_ids', [])]
            print(product_ids)
            # [{'BillNo': 'SM 0117', 'DateTimeP': '02/12/2023, 16:59:58', 'GSTnum': '875643251'}, {'CustomerName': 'arun', 'CustomerNumber': '123456789'}, {'sno': 'Total', 'productName': '0', 'hnsCode': '', 'qty': '0', 'sgstNo': '0.00', 'cgstNo': '0.00', 'amount': '0.00', 'discountAmount': '0.00', 'netAmount': '0.00'}, {'SGST': '', 'DisCount': '', 'Amount': '', 'CGST': '', 'Balance': '', 'GSTAmount': '', 'DisAmount': '', 'TotalAmount': ''}]
            sale_datetime = datetime.strptime(product_ids[0]['DateTimeP'], '%d/%m/%Y, %H:%M:%S')
            print(sale_datetime)
            for sales_product_id in sales_product_ids:
                
                sales_data = {
                    'bill_no':product_ids[0]['BillNo'],
                    'gst_no':product_ids[0]['GSTnum'],
                    'sale_datetime':sale_datetime,
                    'customer_name':product_ids[1]['CustomerName'],
                    'customer_id':'1',
                    # 'customer_id':product_ids[1]['CustomerId'],
                    'customer_phone_number':product_ids[1]['CustomerNumber'],
                    'product_name': sales_product_id['productName'],
                    'hns_code' : sales_product_id['hnsCode'],
                    'quantity': sales_product_id['qty'],
                    'sgst_amount': sales_product_id['sgstNo'],
                    'cgst_amount':sales_product_id['cgstNo'],
                    'amount':sales_product_id['amount'],
                    'discount': sales_product_id['discountAmount'],
                    'total_amount': sales_product_id['netAmount'],
                    # 'payment_type':'Cash'
                   
                }

                # Create a new Sales instance and save it
                sales_instance = Sales_Product(**sales_data)
                sales_instance.save()
            # print(sales_data)
            sale_details={
                    'bill_no':product_ids[0]['BillNo'],
                    'gst_no':product_ids[0]['GSTnum'],
                    'sale_datetime':sale_datetime,
                    'customer_name':product_ids[1]['CustomerName'],
                    'customer_id':'1',
                    # 'customer_id':product_ids[1]['CustomerId'],
                    'customer_phone_number':product_ids[1]['CustomerNumber'],
                    'number_of_products': sales_product_id['sno'],
                    # 'hns_code' : sales_product_id['hnsCode'],
                    'quantity': sales_product_id['qty'],
                    'sgst_amount': sales_product_id['sgstNo'],
                    'cgst_amount':sales_product_id['cgstNo'],
                    'gst_amount':sales_product_id['cgstNo'],
                    'discount_amount': sales_product_id['discountAmount'],
                    'customer_giving_amount': sales_product_id['netAmount'],
                    'balance_given_amount': sales_product_id['discountAmount'],
                    'final_amount': sales_product_id['netAmount'],
                    'payment_type':'Cash'
                   
                }
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(sale_details)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            sale_total = Sales_Product.objects.all()
            sales_list_val = [sale.total_amount for sale in sale_total]
            print(sales_list_val)
            
            # Extract numeric values without Decimal('')
            numeric_values = [float(str(value)) for value in sales_list_val]

            print(numeric_values)
            # Perform addition operation on the numeric values
            total_sum = 0
            for value in numeric_values[:-1]:  # Iterate up to the second-to-last element
                total_sum += value

                print("Total Sum:", total_sum)

            return JsonResponse({'message': 'Sales data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
