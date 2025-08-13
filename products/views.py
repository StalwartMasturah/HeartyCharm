from django.shortcuts import render, get_object_or_404
from .models import Category

# Create your views here.

def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/category_list.html', {'category': category, 'products': products})
