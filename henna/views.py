from django.shortcuts import render, get_object_or_404
from .models import Category, HennaDesign, Product, HomePageContent, AboutPageContent


def home(request):
    featured_designs = HennaDesign.objects.select_related('category').filter(is_featured=True)[:4]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:3]
    page_content = HomePageContent.load()
    return render(request, 'index.html', {
        'featured_designs': featured_designs,
        'featured_products': featured_products,
        'home': page_content,
    })


def about(request):
    page_content = AboutPageContent.load()
    return render(request, 'about.html', {
        'about': page_content,
    })


def gallery(request):
    categories = Category.objects.all()
    selected_slug = request.GET.get('category', '').strip()

    designs = HennaDesign.objects.select_related('category').all()
    if selected_slug and selected_slug != 'all':
        designs = designs.filter(category__slug=selected_slug)

    return render(request, 'gallery.html', {
        'categories': categories,
        'designs': designs,
        'selected_slug': selected_slug or 'all',
    })


def products(request):
    all_products = Product.objects.filter(is_available=True)
    return render(request, 'products.html', {
        'products': all_products,
    })