from django.shortcuts import render
from django.core.paginator import Paginator
import json
from django.shortcuts import render, get_object_or_404,redirect
from .models import Blog, Rate, Comment
from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializes import Blogserializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes,permission_classes
# Create your views here.
def blog_list(request):
    blog_list = Blog.objects.all().order_by('-id')
    paginator = Paginator(blog_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'Blog/index.html',{
        'blog_list': blog_list,
        'page_obj' : page_obj,
        'paginator': paginator,
    })

def search_view(request):

    keyword = request.GET.get("name", "")

    products = Blog.objects.filter(
        author=request.user,
        name__icontains=keyword
    )

    for product in products:
        if product.image:
            product.image = json.loads(product.image)

    return render(
        request,
        "Blog/search.html",
        {
            "products": products,
            "keyword": keyword,
        }
    )

def search_advanced_view(request):
    products = Blog.objects.exclude(
        image__isnull=True
    ).exclude(
        image=""
    )

    name = request.GET.get("name", "").strip()
    price = request.GET.get("price", "")
    category = request.GET.get("category", "")
    brand = request.GET.get("brand", "")
    status = request.GET.get("status", "")

    if name:
        products = products.filter(
            title__icontains=name
        )

    if price:
        min_price, max_price = price.split("-")

        products = products.filter(
            price__range=(min_price, max_price)
        )

    if category:
        products = products.filter(
            category_id=category
        )

    if brand:
        products = products.filter(
            brand_id=brand
        )

    if status in ["0", "1"]:
        products = products.filter(
            status=status
        )

    for product in products:
        try:
            product.image = json.loads(product.image)
        except:
            product.image = []

    

    return render(
        request,
        "Blog/search-advanced.html",
        {
            "products": products,
            
        }
    )

def ajax_search_advanced_view(request):

    products = Blog.objects.filter(
        author=request.user
    ).exclude(
        image__isnull=True
    ).exclude(
        image=""
    )

    name = request.GET.get("name","").strip()
    status = request.GET.get("status","")

    if name:
        products = products.filter(
            name__icontains=name
        )

    if status in ["0", "1"]:
        products = products.filter(
            status=status
        )

    for product in products:
        try:
            product.image = json.loads(product.image)
        except:
            product.image = []

    return render(
        request,
        "Blog/ajax-product-list.html",
        {
            "products": products,
        }
    ) 