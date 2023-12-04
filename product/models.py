from django.db import models
from django.utils.translation import gettext_lazy as _
import pytz  # Add this import statement
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator,RegexValidator

class Account(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True,max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(_("Email"), max_length=254)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_num = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    role = models.CharField(max_length=255)
    Account_date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
            if not self.admin_id:
            # Set the purchase_id to a unique 8-digit value
                last_admin = Account.objects.order_by('-admin_id').first()
                if last_admin:
                    self.admin_id = last_admin.admin_id + 1
                else:
                    self.admin_id = 10000000  # Starting value

            super().save(*args, **kwargs)

    # REQUIRED_FIELDS = ['username']  
    USERNAME_FIELD = 'username'
    class Meta:
            verbose_name = "Account"
            verbose_name_plural = "Accounts"
        
    def __str__(self):
        return self.username
    

class Category(models.Model):
        category_name = models.CharField(max_length=255,unique=True)
        category_code = models.CharField(max_length=255)
        category_id = models.AutoField(primary_key=True)
        category_description = models.TextField()
        category_created = models.DateTimeField()
        category_image = models.FileField(upload_to='uploads/', blank=True, null=True)
        def save(self, *args, **kwargs):
            if not self.category_id:
            # Set the purchase_id to a unique 8-digit value
                last_category = Category.objects.order_by('-category_id').first()
                if last_category:
                    self.category_id = last_category.category_id + 1
                else:
                    self.category_id = 10000000  # Starting value

            super().save(*args, **kwargs) 
        class Meta:
            verbose_name = "Category"
            verbose_name_plural = "Categories"
        
        def __str__(self):
            return self.category_name
        

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255,default=100000000)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_num = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    gst_num = models.PositiveIntegerField()
    invoice_num = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    vendor_id = models.AutoField(primary_key=True)
    vendor_created = models. DateField(auto_now_add=True)
    def save(self, *args, **kwargs):
            if not self.vendor_id:
            # Set the purchase_id to a unique 8-digit value
                last_vendor = Vendor.objects.order_by('-vendor_id').first()
                if last_vendor:
                    self.vendor_id = last_vendor.vendor_id + 1
                else:
                    self.vendor_id = 10000000  # Starting value

            super().save(*args, **kwargs)  
    class Meta:
            verbose_name = "Vendor"
            verbose_name_plural = "Vendors"
        
    def __str__(self) :
         return str(self.vendor_id)


class Product(models.Model):
        product_id = models.AutoField(primary_key=True)
        products_name = models.CharField(max_length=255)
        category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products',to_field='category_name')
        sub_category = models.CharField(max_length=255,)
        brand = models.CharField(max_length=255)
        unit =models.CharField(max_length=40)
        sku = models.CharField(max_length=25)
        vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_products')
        quantity = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        description = models.TextField(max_length=2000)
        gst = models.CharField(max_length=8)
        discount =  models.CharField(max_length=8)
        hsn_code = models.CharField(max_length=30)
        mrp = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        price = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        status = models.CharField(max_length=30,  default='Active')
        product_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
        product_created = models. DateTimeField()
        product_modified = models. DateTimeField(auto_now_add=True)
        total_amount = models.FloatField(max_length=15,  validators=[MinValueValidator(0)], null=True, blank=True)
        def save(self, *args, **kwargs):
            if not self.product_id:
            # Set the purchase_id to a unique 8-digit value
                last_product = Product.objects.order_by('-product_id').first()
                if last_product:
                    self.product_id = last_product.product_id + 1
                else:
                    self.product_id = 10000000  # Starting value

            super().save(*args, **kwargs)          
        
        class Meta:
            verbose_name = "Product"
            verbose_name_plural = "Products"
        
        def __str__(self):
                return str(self.pk)

class Purchase(models.Model): 
        purchases_id = models.AutoField(primary_key=True)
        product_name = models.CharField(max_length=255,)
        category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='purchase_category',to_field='category_name')
        sub_category = models.CharField(max_length=255,)
        brand = models.CharField(max_length=255)
        unit = models.CharField(max_length=40)
        sku = models.CharField(max_length=25)
        vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_vendor')
        quantity = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        description = models.TextField(max_length=2000)
        gst = models.CharField(max_length=8)
        discount =  models.CharField(max_length=8)
        hsn_code = models.CharField(max_length=30)
        mrp = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        price = models.FloatField(validators=[MinValueValidator(0)],max_length=10)
        status = models.CharField(max_length=30,  default='Active')
        product_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
        purchase_created = models. DateTimeField()   
        total_amount = models.FloatField(max_length=15, validators=[MinValueValidator(0)], null=True, blank=True)
        def save(self, *args, **kwargs):
            if not self.purchases_id:
            # Set the purchase_id to a unique 8-digit value
                last_purchases = Purchase.objects.order_by('-purchases_id').first()
                if last_purchases:
                    self.purchases_id = last_purchases.purchases_id + 1
                else:
                    self.purchases_id = 10000000  # Starting value

            super().save(*args, **kwargs)          
        
        class Meta:
            verbose_name = "Purchase"
            verbose_name_plural = "Purchases"
        
        def __str__(self):
                return str(self.pk)

 

    


        

class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    bill_no = models.PositiveIntegerField()
    gst_no = models.CharField(max_length=9)
    sale_datetime = models.DateTimeField()
    customer_name = models.CharField(max_length=255)
    customer_phone_number = models.CharField(max_length=15)
    number_of_products = models.IntegerField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sgst_amount = models.CharField(max_length=20)
    cgst_amount = models.CharField(max_length=20)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    customer_giving_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    balance_given_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_type = models.CharField(max_length=20, default='Cash')
    
    def save(self, *args, **kwargs):
        if not self.sales_id:
            # Set the purchase_id to a unique 8-digit value
            last_sales = Sales.objects.order_by('-sales_id').first()
            if last_sales:
                self.sales_id = last_sales.sales_id + 1
            else:
                self.sales_id = 10000000  # Starting value

        super().save(*args, **kwargs)  
    
    class Meta:
            verbose_name = "Sales"
            verbose_name_plural = "Sales"
    
@receiver(post_save, sender=Sales)
def update_product_quantity(sender, instance, **kwargs):
    # Update the Product quantity when a Sale is made
    try:
        product = Product.objects.get(products_name=instance.product_name)
        product.qty -= instance.quantity
        product.save()
    except Product.DoesNotExist:
        return 'Product does not available'
    


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    customer_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    customer_created=  models. DateTimeField() 
    def save(self, *args, **kwargs):
        if not self.customer_id:
            # Set the purchase_id to a unique 8-digit value
            last_customer = Customer.objects.order_by('-customer_id').first()
            if last_customer:
                self.customer_id = last_customer.customer_id + 1
            else:
                self.customer_id = 10000000  # Starting value

        super().save(*args, **kwargs)  
    
     # Validators should be a list    customer_created = models.DateTimeField(auto_now_add=True)
    class Meta:
            verbose_name = "Customer"
            verbose_name_plural = "Customer"



class Sales_Product(models.Model):
    sales_products_id = models.AutoField(primary_key=True)
    bill_no = models.CharField(max_length=20)
    gst_no = models.CharField(max_length=9)
    sale_datetime = models.DateTimeField()
    customer_name = models.CharField(max_length=255)
    customer_phone_number = models.CharField(max_length=15)
    customer_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    hns_code  = models.CharField(max_length=9) 
    quantity = models.PositiveIntegerField()
    sale_product_datetime = models.DateTimeField(auto_now_add=True)
    cgst_amount = models.CharField(max_length=9) 
    sgst_amount = models.CharField(max_length=9) 
    amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    discount = models.CharField(max_length=9) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    def save(self, *args, **kwargs):
        if not self.sales_products_id:
            # Set the purchase_id to a unique 8-digit value
            last_sales_products = Sales_Product.objects.order_by('-sales_products_id').first()
            if last_sales_products:
                self.sales_products_id = last_sales_products.sales_products_id + 1
            else:
                self.sales_products_id = 10000000  # Starting value

        super().save(*args, **kwargs)  
    
    class Meta:
            verbose_name = "Sales_product"
            verbose_name_plural = "Sales_product"
