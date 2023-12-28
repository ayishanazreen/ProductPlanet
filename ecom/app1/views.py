from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import product, cart, Payment, order_placed, Wishlist
from .forms import CustomerRegistrationForm, customerProfileForm
from django.contrib import messages
from django.db.models import Q
from .models import customer
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
      totalitem=len(cart.objects.filter(user=request.user))
      wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,'home.html',locals())

@login_required
def about(request):
  totalitem=0
  wishitem=0
  if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
  return render(request,'about.html',locals())

@login_required
def contact(request):
  totalitem=0
  wishitem=0
  if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
  return render(request,'contact.html',locals())


class userRegistration(View):
  def get(self,request):
    form=CustomerRegistrationForm()
    return render(request,'userCreation.html',locals())
  def post(self,request):
   form=CustomerRegistrationForm(request.POST)
   if form.is_valid():
     form.save()
     messages.success(request,"User Registered Successfully")
   else:
     messages.warning(request,"Invalid Input")
   return render(request,'userCreation.html',locals())
  

@method_decorator(login_required,name='dispatch')
class login(View):
   def get(self,request):
    return render(request,'login.html',locals()) 
   def post(self,request):
    return render(request,'login.html',locals()) 


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
     totalitem=len(cart.objects.filter(user=request.user))
     wishitem=len(Wishlist.objects.filter(user=request.user))
    form=customerProfileForm()
    return render(request,'profile.html',locals()) 
  def post(self,request):
    form=customerProfileForm(request.POST)
    if form.is_valid():
      user=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      mobile=form.cleaned_data['mobile']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
      reg.save()
      form=customerProfileForm(request.POST)
      messages.success(request,"profile created successfully")
    else:
      messages.warning(request,"profile does not created successfully")
      form=customerProfileForm()
    return render(request,'profile.html',locals()) 
  
@login_required
def address(request):
  totalitem=0
  wishitem=0
  if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
  add=customer.objects.filter(user=request.user)
  return render(request,'address.html',locals())  

@method_decorator(login_required,name='dispatch')
class update_address(View):
  def get(self,request,pk):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
     totalitem=len(cart.objects.filter(user=request.user))
     wishitem=len(Wishlist.objects.filter(user=request.user))
    add=customer.objects.get(pk=pk)
    form=customerProfileForm(instance=add)
    return render(request,'update_address.html',locals()) 
  def post(self,request,pk):
    form=customerProfileForm(request.POST)
    if form.is_valid():
      add=customer.objects.get(pk=pk)
      add.name=form.cleaned_data['name']
      add.locality=form.cleaned_data['locality']
      add.city=form.cleaned_data['city']
      add.mobile=form.cleaned_data['mobile']
      add.state=form.cleaned_data['state']
      add.zipcode=form.cleaned_data['zipcode']
      add.save()
      messages.success(request,"Profile updated Successfully")
    else:
      messages.warning(request,"invalid entry")
    return redirect("address") 

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
  def get(self,request,val):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
     totalitem=len(cart.objects.filter(user=request.user))
     wishitem=len(Wishlist.objects.filter(user=request.user))
    prod=product.objects.filter(category=val)
    return render(request,'product_view.html',locals()) 


@method_decorator(login_required,name='dispatch')  
class CategoryTitle(View):
  def get(self,request,val):
   totalitem=0
   wishitem=0
   if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
    prod=product.objects.filter(title=val)
    title=product.objects.filter(category=prod[0].category).values('title')
    return render(request,'product_view.html',locals())
    
@method_decorator(login_required,name='dispatch')
class Product_Details(View):
 def get(self,request,pk):
     prod=product.objects.get(pk=pk)
     wishlist=Wishlist.objects.filter(Q(products=prod) & Q(user=request.user))
     totalitem=0
     wishitem=0
     if request.user.is_authenticated:
       totalitem=len(cart.objects.filter(user=request.user))
       wishitem=len(Wishlist.objects.filter(user=request.user))
     return render(request,'product_details.html',locals())   


@login_required
def add_cart(request):
 user=request.user
 prod_id=request.GET.get('prod_id')
 products=product.objects.get(id=prod_id)
 cart(user=user,products=products).save()
 return redirect("/show_cart")

@login_required
def show_cart(request):
  totalitem=0
  wishitem=0
  if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
  user=request.user
  ct=cart.objects.filter(user=user)
  amount=0
  for p in ct:
    value = p.quantity* p.products.discounted_price
    amount=amount + value
  totalamount=amount + 40
  return render(request,'add_cart.html', locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
  def get(self, request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
      totalitem=len(cart.objects.filter(user=request.user))
      wishitem=len(Wishlist.objects.filter(user=request.user))
    add=customer.objects.filter(user=request.user)
    cart_item=cart.objects.filter(user=request.user)
    amount=0
    for p in cart_item:
       value = p.quantity* p.products.discounted_price
       amount=amount + value
    totalamount=amount + 40
    razoramount=int(totalamount * 100)
    client=razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11" }
    payment_response = client.order.create(data=data)
    print(payment_response)

     #{'id': 'order_NE32Bm8RHa9Ez6', 'entity': 'order', 'amount': 603800, 'amount_paid': 0, 'amount_due': 603800, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1702954841}
   
    order_id=payment_response['id']
    order_status=payment_response['status']
    if order_status=='created':
      payment=Payment(
        user=request.user,
        amount=totalamount,
        razorpay_order_id=order_id,
        razorpay_payment_status=order_status,
      )
      payment.save()

    return render(request,"checkout.html",locals())
  
@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    cust=customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)  
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    ct=cart.objects.filter(user=user)
    for c in ct :
      order_placed(user=user,cust=cust,products=c.products,quantity=c.quantity,payment=payment).save()
      c.delete()
    return redirect("orders")  


@login_required
def orders(request):
  totalitem=0
  wishitem=0
  if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
  order=order_placed.objects.filter(user=request.user)
  return render(request, 'orders.html', locals())



@login_required
def search(request):
   totalitem=0
   wishitem=0
   if request.user.is_authenticated:
    totalitem=len(cart.objects.filter(user=request.user))
    wishitem=len(Wishlist.objects.filter(user=request.user))
   query=request.GET.get('search')
   products=product.objects.filter(Q(title__icontains=query))
   return render(request, 'search.html',locals())



def plus_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c=cart.objects.get(Q(products=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    user=request.user
    ct=cart.objects.filter(user=user)
    amount=0
  for p in ct:
    value = p.quantity* p.products.discounted_price
    amount=amount + value
  totalamount=amount + 40
  data={
    "quantity":c.quantity,
    "amount":amount,
    "totalamount":totalamount
  }
  return JsonResponse(data)



def minus_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c=cart.objects.get(Q(products=prod_id) & Q(user=request.user))
    c.quantity=c.quantity-1
    c.save()
    user=request.user
    ct=cart.objects.filter(user=user)
    amount=0
  for p in ct:
    value = p.quantity * p.products.discounted_price
    amount=amount + value
  totalamount=amount + 40
  data={
    "quantity":c.quantity,
    "amount":amount,
    "totalamount":totalamount
  }
  return JsonResponse(data)


def remove_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c=cart.objects.get(Q(products=prod_id) & Q(user=request.user))
    c.delete()
    user=request.user
    ct=cart.objects.filter(user=user)
    amount=0
  for p in ct:
    value = p.quantity * p.products.discounted_price
    amount=amount + value
  totalamount=amount + 40
  data={
    "amount":amount,
    "totalamount":totalamount
  }
  return JsonResponse(data)


def plusWishlist(request):
  if request.method=='GET':
    prod_id=request.GET.get("prod_id")
    products=product.objects.get(id=prod_id)
    user=request.user
    Wishlist(user=user, products=products).save()
    data={
      'message':'Wishlist added Successfully'
    }
    return JsonResponse(data)


def minusWishlist(request):
  if request.method=='GET':
    prod_id=request.GET.get("prod_id") 
    products=product.objects.get(id=prod_id)
    user=request.user
    Wishlist.objects.filter(user=user,products=products).delete()
    data={
      'message':'Wishlist removed Successfully'
    }
    return JsonResponse(data)
  

def wishlist(request):
  wish=Wishlist.objects.filter(user=request.user)
  return render(request,'wishlist.html',locals())  