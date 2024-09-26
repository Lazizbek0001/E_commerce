from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, ShippingAddress, PaymentForm
from django.contrib import messages
from payment.models import Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product
# Create your views here.

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        return render(request, 'payment/orders.html', {'order':order,'items':items})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        orders = Order.objects.filter(shipped=False)
        
        
        
        
        return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders':orders})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products= cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        payment_form = PaymentForm(request.POST or None)
        # Get shipping Session Data
        my_shipping = request.session.get('my_shipping')
        
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create shipping Address from session info
        shipping_address = f"""{my_shipping['shipping_address1']}
{my_shipping['shipping_address2']}
{my_shipping['shipping_city']}
{my_shipping['shipping_state']}
{my_shipping['shipping_zipcode']}
{my_shipping['shipping_country']}"""
        amount_paid = totals
        
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name,email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            
            order_id = create_order.pk
            # Get product id
            for product in cart_products():
                
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id , product_id= product_id, user= user, quantity= value, price=price)
                        create_order_item.save()
                        
            # delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                    
                
                                 
            messages.success(request,"Order Placed")
            return redirect('home')
        else:
            create_order = Order(full_name=full_name,email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            order_id = create_order.pk
            # Get product id
            for product in cart_products():
                
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price - product.price
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id , product_id= product_id, quantity= value, price=price)
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            messages.success(request,"Order Placed")
            return redirect('home')
        
    else:
        messages.success(request,"Access Denied")
        return redirect('home')

def billing_info(request):
    if request.POST:
        
        cart = Cart(request)
        cart_products= cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Create session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        if request.user.is_authenticated:
            # get the billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals, 'shipping_info':request.POST,'billing_form':billing_form})
            
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products':cart_products,"quantities":quantities,'totals':totals, 'shipping_info':request.POST,'billing_form':billing_form})
           
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

