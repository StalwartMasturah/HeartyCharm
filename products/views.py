from django.shortcuts import render, get_object_or_404,redirect,render
from .models import Category, Product, Order
from .forms import CheckoutForm
from .forms import CustomOrderForm
from django.contrib import messages
from .cart import Cart
from django.core.paginator import Paginator
import uuid
from django.conf import settings
from django.urls import reverse
import requests



def shop_home(request):
    categories = Category.objects.all()
    return render(request, 'products/shop.html', {
        'categories': categories
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category=category, stock__gt=0)

    paginator = Paginator(product_list, 8)  # products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # If this is the "custom orders" category, redirect to a form
    if category.slug == "gift-custom-orders":
        return redirect('custom_order_form')   
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

def custom_order_form(request):
    if request.method == "POST":
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            # Here you can save the order to the database or send an email
            # For now, we'll just show a success message
            messages.success(request, "Your custom order has been submitted!")
            return redirect('products')  # redirect back to products
    else:
        form = CustomOrderForm()

    return render(request, 'products/custom_order_form.html', {'form': form})
 
 
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart_detail')

def update_cart(request, product_id, action):
    """
    Handle increasing or decreasing quantity in session cart.
    action = 'increase' or 'decrease'
    """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    # Find current quantity
    current_qty = 0
    for item in cart.get_items():
        if item['product'].id == product.id:
            current_qty = item['quantity']
            break

    if action == 'increase':
        cart.add(product, quantity=1)
    elif action == 'decrease' and current_qty > 1:
        cart.add(product, quantity=-1)

    return redirect('cart_detail')  # or redirect(request.META.get('HTTP_REFERER', 'shop'))

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'products/cart.html', {'cart_items': cart.get_items(), 'total': cart.get_total_price()})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop')

    total = 0
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * item['quantity']

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_price=total
            )

            # redirect to payment
            return redirect('start_payment', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'products/checkout.html', {
        'form': form,
        'total': total
    })
 
 
# def cart_view(request):
#     cart = request.session.get('cart', {})
#     items = []
#     total = 0

#     for product_id, item in cart.items():
#         product = Product.objects.get(id=product_id)
#         quantity = item['quantity']
#         price = product.price * quantity
#         total += price

#         items.append({
#             'product': product,
#             'quantity': quantity,
#             'price': price
#         })

#     form = CheckoutForm()

#     return render(request, 'products/cart.html', {
#         'items': items,
#         'total': total,
#         'form': form,
      
#     })
from .cart import Cart

def cart_view(request):
    cart = Cart(request)

    return render(request, 'products/cart.html', {
        'cart_items': cart.get_items(),
        'total': cart.get_total_price(),
    })

# def cart_view(request):
#     cart = request.session.get('cart', {})

#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)
#         if form.is_valid():
#             # redirect to payment verification page
#             return redirect('verify_payment')


def start_payment(request, order_id):
    order = Order.objects.get(id=order_id)

    reference = str(uuid.uuid4())
    order.payment_reference = reference
    order.save()

    amount = int(order.total_price * 100) 

    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
        'reference': reference,
        'amount': amount,
    }

    return render(request, 'products/paystack.html', context)

  

def verify_payment(request):
    reference = request.GET.get('reference')

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    if result['status'] and result['data']['status'] == 'success':
        order = Order.objects.get(payment_reference=reference)
        order.payment_status = 'paid'
        order.save()

        request.session['cart'] = {}  # clear cart

        return redirect('payment_success')

    return redirect('checkout')


def payment_success(request):
    return render(request, 'products/payment_success.html')

