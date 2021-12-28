from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Product , Cart , Address , OrderPlaced
from django.contrib.auth.models import User
from .forms import SignUpForm , LoginForm , AddressForm , CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
from django.db.models import Q


def all_products(request):
    products=Product.objects.all()
    trending=Product.objects.all().order_by('price')[:7]
    return render(request , 'accounts/all_products.html',{'products':products,'trending':trending})

def product_detail(request , slug):
    product=Product.objects.get(pk=slug)
    sp=product.price-int(product.price/10)
    return render(request , 'accounts/product_detail.html',{'product':product,'sp':sp})

def categories(request , slug):
    print("SLUG",slug)
    products=Product.objects.filter(category=slug)
    return render(request , 'accounts/category.html',{'products':products,'slug':slug})


# USER AUTH

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=SignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Account Created')
                return HttpResponseRedirect('/signup/')
        else:
            fm=SignUpForm()
        return render(request , 'accounts/signup.html',{"form":fm})
    else:
        return HttpResponseRedirect('/profile/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm=LoginForm(request=request , data=request.POST)
            if fm.is_valid():
                name=fm.cleaned_data['username']
                password=fm.cleaned_data['password']
                user=authenticate(username=name , password=password)
                if user is not None:
                    login(request , user)
                    return HttpResponseRedirect('/profile/')
        else:
            fm=LoginForm()
        return render(request , 'accounts/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def user_profile(request):
    if request.user.is_authenticated:
        addresses=Address.objects.filter(user=request.user)
        return render(request , 'accounts/profile.html',{'addresses':addresses})
    else:
        return HttpResponseRedirect('/login/')



def add_address(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=AddressForm(request.POST)
            if fm.is_valid():
                user=request.user
                locality=request.POST.get('locality')
                city=request.POST.get('city')
                state=request.POST.get('state')
                pincode=request.POST.get('pincode')
                # print(f'User :{user} Locality {locality} city {city} state {state} pincode {pincode} ')
                addr=Address(user=user,locality=locality,city=city,state=state,pincode=pincode)
                addr.save()
                messages.success(request , 'Address Added Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm=AddressForm()
        return render(request , 'accounts/add_address.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')


def search_product(request):
    print('get request')
    product_name=request.GET.get('product_name')
    try:
        products=Product.objects.filter(title__icontains=product_name).values()
    except:
        product=None
    products_list=list(products)
    return JsonResponse({'status':1,'product_list':products_list})

def change_password(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=CustomPasswordChangeForm(user=request.user , data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request , fm.user)
                messages.success(request , 'Password Changed Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm=CustomPasswordChangeForm(user=request.user)
        return render(request , 'accounts/change_password.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

    
def add_to_cart(request):
    if request.user.is_authenticated:
        product_title=request.GET.get('prod_id')
        product=Product.objects.get(title=product_title)
        print(product)
        carts=None
        # We can CART an item Only Once
        try:
            carts=Cart.objects.get(Q(user=request.user) & Q(product=product))
            print(carts)
        except:  
            print(carts)
            user=request.user
            Cart(user=request.user , product=product).save()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/login/')

def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        carts=Cart.objects.filter(user=user)
        flag=True
        amount=0.0
        shipping_amount=45
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                temp_amount=float((p.qty * (p.product.price-int(p.product.price/10))))
                amount+=temp_amount
        # print(amount)
        # print("************************************")
        total_amount=amount+shipping_amount
        if(amount==0.0):
            flag=False
        addresses=Address.objects.filter(user=request.user)
        return render(request , 'accounts/show_cart.html',{'carts':carts,'total_amount':total_amount,'shipping_amount':shipping_amount,'product_amount':amount,'flag':flag,'addresses':addresses})
    else:
        return HttpResponseRedirect('/login/')

def remove_item(request , id):
    if request.user.is_authenticated:
        product=Product.objects.get(pk=id)
        cart_row=Cart.objects.get(Q(product=product) & Q(user=request.user))
        cart_row.delete()
        return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/login/')


def checkout(request):
    if request.user.is_authenticated:
        user=request.user
        carts=Cart.objects.filter(user=user)
        print(carts)
        address_id=request.GET.get('address-id')
        print(address_id)
        address=Address.objects.get(pk=address_id)
        print(address)
        for cart in carts:
            OrderPlaced(user=request.user , product=cart.product , address=address).save()
            cart.delete()
        orders=OrderPlaced.objects.filter(user=request.user)
        return render(request , 'accounts/orders.html',{'orders':orders})
    else:
        return HttpResponseRedirect('/login/')


def orders(request):
    if request.user.is_authenticated:
        try:
            orders=OrderPlaced.objects.filter(user=request.user)
        except:
            return HttpResponseRedirect('/cart/')
        print(orders)
        return render(request , 'accounts/orders.html',{'orders':orders})
    else:
        return HttpResponseRedirect('/login/')