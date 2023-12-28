from django.db import models
from django.contrib.auth.models import User

# Create your models here.
category_choices=(
    ('LP','Laptop'),  
    ('MS','Mouse'),
    ('LN','LAN'),
    ('TB','Tablet'),
    ('KB','Keyboard'),
    )
STAT_CHOICES=(
     ('Kerala','kerala'),
     ('Tamilnadu','Tamilnadu'),
     ('Karnataka','Karnataka'),
     ('Andhra Pradesh','Andhra Pradesh'),
     ('Goa','Goa'),
     ('Maharashtra','Maharashtra'),
)
STATUS_CHOICES=(
      ('Accepted','Accepted'),
      ('Packed','Packed'),
      ('On the Way','On the Way'),
      ('Delivered','Delivered'),
      ('Cancel','Cancel'),
      ('Pending','Pending'),
 )    

class product(models.Model):
    title=models.CharField(max_length=30)
    orginal_price=models.IntegerField()
    discounted_price=models.IntegerField()
    desc=models.TextField(max_length=200)
    features=models.TextField(max_length=100)
    category=models.CharField(choices=category_choices,max_length=2)
    product_image=models.ImageField(upload_to='products')
  
    def __str__(self):
         return self.title
    
class customer(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)  
     name=models.CharField(max_length=200)
     locality=models.CharField(max_length=200)
     city=models.CharField(max_length=200)
     mobile=models.IntegerField(default=0)
     zipcode=models.IntegerField()
     state=models.CharField(choices=STAT_CHOICES, max_length=100)

     def __str__(self):
         return self.name


class cart(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     products=models.ForeignKey(product,on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=1)


     @property
     def total_cost(self):
          return self.quantity * self.pro.discounted_price


class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100, blank=True, null=True)    
    razorpay_payment_status=models.CharField(max_length=100, blank=True, null=True) 
    razorpay_payment_id=models.CharField(max_length=100, blank=True, null=True) 
    paid=models.BooleanField(default=False)
    @property
    def total_cost(self):
      return self.quantity * self.pro.discounted_price


class order_placed(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     cust=models.ForeignKey(customer, on_delete=models.CASCADE)
     products=models.ForeignKey(product,on_delete=models.CASCADE)
     quantity=models.PositiveIntegerField(default=1)    
     ordered_date=models.DateTimeField(auto_now_add=True)
     status=models.CharField(max_length=40,choices=STATUS_CHOICES, default="Pending")
     payment=models.ForeignKey(Payment,on_delete=models.CASCADE, default="")

     @property
     def total_cost(self):
          return self.quantity * self.pro.discounted_price
     
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(product,on_delete=models.CASCADE)
