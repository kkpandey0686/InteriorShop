import random

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddToCartForm, WriteReviewForm, MaxDistanceForm
from .models import Category, Product, ProductReview

from apps.cart.cart import Cart

import copy

from apps.userapp.distance import distance

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    lat_user = 19.2362
    long_user = 73.1302
    max_distance = 1000

    if request.method=='POST':
        max_distance_form = MaxDistanceForm(request.POST)

        if max_distance_form.is_valid():
            max_distance = max_distance_form.cleaned_data['max_distance']

    else:
        max_distance_form = MaxDistanceForm()

    if request.user.is_authenticated:
        lat_user = request.user.customUser.latitude
        long_user = request.user.customUser.longitude
    
    distance_list =[]

    for product in products:
        lat_vendor = product.vendor.created_by.customUser.latitude
        long_vendor = product.vendor.created_by.customUser.longitude
        

        d = distance(lat_user,lat_vendor,long_user,long_vendor)

        t = (product,round(d))
        distance_list.append(t)


    return render(request, 'product/search.html', {'distance_list': distance_list ,'query': query, 'max_distance': max_distance})

def product(request, category_slug, product_slug):
    # if request.user.customUser.role not in {'VEN', 'CUS'}:
    #     form = RegisterForm()
    #     return render(request, 'core/accessdenied.html', {'form': form})

    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method=='POST' and 'write_review' in request.POST:
        review_form = WriteReviewForm(request.POST)
        form = AddToCartForm()

        if review_form.is_valid():
            review_data = review_form.save(commit=False)
            review_data.product = product
            review_data.user = request.user
            review_data.save()

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    

    if request.method == 'POST' and 'write_review' not in request.POST:
        form = AddToCartForm(request.POST)
        review_form = WriteReviewForm()

        if form.is_valid():
            if product.wholesale and request.user.customUser.role=='CUS':
                messages.error(request, "This product is only available for vendors")
            else:
                quantity = form.cleaned_data['quantity']
                print(quantity)
                if request.user.customUser.role=='VEN':
                    if product.wholesale:
                        if quantity>product.quantity:
                            messages.error(request, "Quantity exceeds than stock")
                        else:
                            cart.add(product_id=product.id, quantity=quantity)
                            messages.success(request, 'The product was added to the cart')   
                    else:
                        messages.error(request, "You are not authorized for this transaction")
                        return redirect('product', category_slug=category_slug, product_slug=product_slug)
                else:
                    print(quantity)
                    cart.add(product_id=product.id, quantity=quantity)
                    messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
    else:
        form = AddToCartForm()
        review_form = WriteReviewForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    review_list = ProductReview.objects.filter(product=product)

    return render(request, 'product/product.html', {'form': form, 'product': product, 'quantity':product.quantity,'similar_products': similar_products, 'review_form': review_form, 'review_list': review_list})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    lat_user = 19.2362
    long_user = 73.1302

    if request.user.is_authenticated:
        lat_user = request.user.customUser.latitude
        long_user = request.user.customUser.longitude
    
    distance_list =[]

    for product in category.products.all():
        lat_vendor = product.vendor.created_by.customUser.latitude
        long_vendor = product.vendor.created_by.customUser.longitude
        

        d = distance(lat_user,lat_vendor,long_user,long_vendor)

        t = (product,round(d))
        distance_list.append(t)
        

    return render(request, 'product/category.html',{'distance_list':distance_list})


