from django.shortcuts import render
from apps.order.models import Order
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.

def updateStatus(request, id):
    order = Order.objects.get(id = id)
    order.status+=1
    if order.status>=3:
        order.status = 3
    order.save()
    return redirect('vendor_admin')
