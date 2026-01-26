from django.shortcuts import render, get_object_or_404,redirect,render
from .models import Category, Product
from .forms import CustomOrderForm
from django.contrib import messages
from .cart import Cart

def shop_home(request):
    categories = Category.objects.all()
    return render(request, 'products/shop.html', {
        'categories': categories
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    # If this is the "custom orders" category, redirect to a form
    if category.slug == "gift-custom-orders":
        return redirect('custom_order_form')  # we'll create this URL next


    products = category.products.filter(stock__gt=0)

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
            return redirect('shop')  # redirect back to shop
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
