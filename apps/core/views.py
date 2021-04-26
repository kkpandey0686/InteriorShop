from django.shortcuts import render
from apps.userapp.distance import distance
from apps.product.models import Product

def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    lat_user = 19.2362
    long_user = 73.1302

    if request.user.is_authenticated:
        lat_user = request.user.customUser.latitude
        long_user = request.user.customUser.longitude
    
    distance_list =[]

    for product in newest_products:
        lat_vendor = product.vendor.created_by.customUser.latitude
        long_vendor = product.vendor.created_by.customUser.longitude
        

        d = distance(lat_user,lat_vendor,long_user,long_vendor)

        t = (product,round(d))
        distance_list.append(t)


    return render(request, 'core/frontpage.html', {'distance_list': distance_list})

def contact(request):
    return render(request, 'core/contact.html')