from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, ShippingAddress, PaymentForm
from django.contrib import messages
# Create your views here.
def billing_info(request):
    if request.POST:
        
        cart = Cart(request)
        cart_products= cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        if request.user.is_authenticated:
            # get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals, 'shipping_info':request.POST,'billing_form':billing_form})
            
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals, 'shipping_info':request.POST,'billing_form':billing_form})
           
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals,'shipping_form':shipping_form})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
def checkout(request):
    cart = Cart(request)
    cart_products= cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals,'shipping_form':shipping_form})
    else:
        # checkut as guest
        shipping_form = ShippingForm(request.POST or None)
        
        return render(request, 'payment/checkout.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals,'shipping_form':shipping_form})

def payment_success(request):
    
    return render(request, "payment/payment_success.html", {})

