from django.contrib import admin
from .models import product, customer, cart, order_placed, Payment, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
# Register your models here

class productModelAdmin(admin.ModelAdmin):
    list_display=('id','title','discounted_price','desc','features','category')

admin.site.register(product,productModelAdmin)


class customerModelAdmin(admin.ModelAdmin):
    list_display=('id','user','name','locality','city','zipcode','state')

admin.site.register(customer,customerModelAdmin)

@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display=('id','user','disp_products','quantity')
    def disp_products(self, obj):
      link= reverse("admin:app1_product_change",args=[obj.products.pk])
      return format_html('<a href="{}">{}</a>', link, obj.products.title)


class OrderAdmin(admin.ModelAdmin):
    list_display=('id','user','disp_customers','disp_products','quantity', 'ordered_date','status','disp_payment')
    def disp_products(self, obj):
      link= reverse("admin:app1_product_change",args=[obj.products.pk])
      return format_html('<a href="{}">{}</a>', link, obj.products.title)
    
    def disp_customers(self, obj):
      link= reverse("admin:app1_customer_change",args=[obj.cust.pk])
      return format_html('<a href="{}">{}</a>', link, obj.cust.name)
    
    def disp_payment(self, obj):
      link= reverse("admin:app1_payment_change",args=[obj.payment.pk])
      return format_html('<a href="{}">{}</a>', link, obj.payment.razorpay_payment_id)

admin.site.register(order_placed,OrderAdmin)


class paymentAdmin(admin.ModelAdmin):
    list_display=('id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid')

admin.site.register(Payment,paymentAdmin)


class wishlistAdmin(admin.ModelAdmin):
    list_display=('id','user','disp_products')
    def disp_products(self, obj):
      link= reverse("admin:app1_product_change",args=[obj.products.pk])
      return format_html('<a href="{}">{}</a>', link, obj.products.title)

admin.site.register(Wishlist,wishlistAdmin)

admin .site.unregister(Group)


