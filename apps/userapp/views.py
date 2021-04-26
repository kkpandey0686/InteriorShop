from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404

from apps.product.models import Product
from .models import CustomUser
from apps.vendor.models import Vendor

from .forms import RegisterForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            role = data['role']
            latitude = data['latitude']
            longitude = data['longitude']

            user = User()
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            

            customuser = CustomUser()
            customuser.user = user
            customuser.role =role
            customuser.contact = phone
            customuser.address = address
            customuser.zipcode = zipcode
            customuser.latitude = latitude
            customuser.longitude = longitude
        
            #generate otp
            #customUser.otp = otp
            #sendsms(otp)
            user.save()
            customuser.save()

            if role=='VEN' or role=='WHO':
                vendor = Vendor.objects.create(name=first_name, created_by=user)
                vendor.save()

            login(request, user)

            if role=='VEN' or role=='WHO':
                return redirect('vendor_admin')
            
            if role=='CUS':
                return redirect('frontpage')

            return redirect('frontpage')
    else:
        form = RegisterForm()

    return render(request, 'userapp/signup.html', {'form': form})


@login_required
def user_orders(request):
    if request.user.customUser.role!='CUS':
        form = RegisterForm()
        return render(request, 'core/accessdenied.html', {'form': form})

    user = request.user
    orders = user.orders.all()

    data = []
    for order in orders:
        price = 0
        quantity = 0
        total = 0

        dic =[]
        dic.append(order)
        temp = []
        for item in order.items.all():
            print(item)
            price+= item.price
            quantity+= item.quantity
            total += item.get_total_price()
            temp.append([item.product.title, price, quantity, total])
        dic.append(temp) 
        data.append(dic)

    return render(request, 'userapp/userAdmin.html', {'data':data})
