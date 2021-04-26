import stripe 

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_customer, notify_vendor
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.product.models import Product
from apps.product.models import Category

import copy

@login_required
def cart_detail(request):
    if request.user.customUser.role!='CUS' and request.user.customUser.role!='VEN':
        return render(request, 'core/accessdenied.html')

    cart = Cart(request)
    cartBasket = cart.cart
    print(cartBasket)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        checkQuantity = True
        cartClone = copy.deepcopy(cartBasket)
        wholeSaleFlag = False

        for productID in cartBasket:
            product = Product.objects.get(id=productID)
            if product.wholesale:
                wholeSaleFlag = True
            available_quantity = product.quantity
            if cartBasket[productID]['quantity']>available_quantity:
                checkQuantity = False
      
        if checkQuantity is False:
            print("exceeded")
            messages.error(request,'Product quantity exceeded')
            return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

        if form.is_valid() and checkQuantity is True:
            try:

                user = request.user
                first_name = user.first_name
                last_name = user.last_name
                email = user.email
                phone = user.customUser.contact
                address = user.customUser.address
                zipcode = user.customUser.zipcode

                print("user details")

                if wholeSaleFlag and request.user.customUser.role=='CUS':
                    messages.error(request, "This product is only available for vendors")
                    return render(request, 'core/accessdenied.html')
                else:
                    if request.user.customUser.role=='VEN':
                        if wholeSaleFlag:
                            for productID in cartBasket:
                                product = Product.objects.get(id=productID)
                                # product.quantity-=cartBasket[productID]['quantity']
                                # product.save()
                                vendorProd = Product()
                                vendorProd.title = product.title
                                vendorProd.price = product.price
                                vendorProd.image = product.image
                                vendorProd.slug = slugify(product.title)
                                vendorProd.category = Category.objects.get(id=product.category.id)
                                vendorProd.description = product.description
                                vendorProd.quantity = cartBasket[productID]['quantity']
                                vendorProd.vendor = request.user.vendor
                                vendorProd.wholesale = False
                                vendorProd.save()
                                print("object added")
                        else:
                            messages.error(request, "You are not authorized for this transaction")
                            return render(request, 'core/accessdenied.html')
                            print("here")
                    else:
                        print("here2")
                        order = checkout(request, first_name, last_name, email, address, zipcode, "place", phone, cart.get_total_cost(), user)
                        
                        print(order)
                        cart.clear()

                        # notify_customer(order)
                        # notify_vendor(order)
            except Exception as e:
                print("here3")
                messages.error(request, 'There was something wrong with the payment')
                print("exception in payment", e)
            else:
                for productID in cartClone:
                    product = Product.objects.get(id=productID)
                    product.quantity -= cartClone[productID]['quantity']
                    product.save()

                return redirect('success')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

def success(request):
    return render(request, 'cart/success.html')