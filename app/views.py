# from itertools import product
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from app.models import Product
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')

        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops})

class ProductDetailView(View):
    def get(self,request, pk):
        product = Product.objects.get(pk = pk)
        return render(request,'app/productdetail.html',{'product':product})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total = 0.0
        # cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart:
            for p in cart:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'amount':amount,'shipping_amount':shipping_amount})
        else:
            return render(request,'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart = Cart.objects.filter(user=request.user) 
        for p in cart:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
            total_amount = amount + shipping_amount

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':total_amount,
                }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart = Cart.objects.filter(user=request.user) 
        for p in cart:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
            total_amount = amount + shipping_amount

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':total_amount,
                }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart = [p for p in Cart.objects.all() if p.user == request.user]
        # cart = Cart.objects.filter(user=request.user) 
        for p in cart:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
            total_amount = amount + shipping_amount

            data = {    
                'amount':amount,
                'total_amount':total_amount,
                }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'activate':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')
    
def mobile(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand='Redmi')
    elif data == 'Apple':
        mobiles = Product.objects.filter(category='M').filter(brand='Apple')
    elif data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand='Oppo')
    elif data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand='Vivo')
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegisterationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'User Successfully Registered')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForms()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForms(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
