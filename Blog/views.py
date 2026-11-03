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

def blog_detail(request,id):

    blog = get_object_or_404(Blog, id=id)

    avg_rate = Rate.objects.filter(
        blog=blog
    ).aggregate(Avg('rate'))

    avg = avg_rate['rate__avg']

    if avg is None:
        avg = 0

    avg = round(avg)

    user_rate = 0

    if request.user.is_authenticated:

        rate_obj = Rate.objects.filter(
            blog=blog,
            user=request.user
        ).first()

        if rate_obj:

            user_rate = rate_obj.rate

    comment = Comment.objects.filter(
        blog_id = id,
        level=0
    ).order_by('-id')

    return render(request, 'Blog/blog_detail.html',{

        'blog': blog,

        'avg': avg,

        'user_rate': user_rate,

        'comment' : comment

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

@csrf_exempt
def save_rating(request):

    if request.method == 'POST':

        blog_id = request.POST.get('blog_id')

        rate = request.POST.get('rate')

        user_id = request.POST.get('user_id')
        print(user_id)

        try:

            blog = Blog.objects.get(id=blog_id)

            old_rate = Rate.objects.filter(
                blog_id=blog_id,
                user_id=user_id
            ).first()

            if old_rate:

                old_rate.rate = int(rate)

                old_rate.save()

            else:

                Rate.objects.create(
                    blog_id=blog_id,
                    rate=int(rate),
                    user_id=user_id
                )

            avg = Rate.objects.filter(
                blog_id=blog_id
            ).aggregate(Avg('rate'))

            return JsonResponse({

                'success': True,

                'avg': round(avg['rate__avg'],1)

            })

        except Blog.DoesNotExist:

            return JsonResponse({

                'success': False,

                'error': 'Blog not found'

            })

    return JsonResponse({

        'success': False,

        'error': 'Invalid request'

    })

@csrf_exempt
def save_comment(request):
    if request.method== "POST":
        blog_id= request.POST.get('blog_id')
        comment = request.POST.get('comment')
        level = request.POST.get('level',0)
        parent_id = request.POST.get('parent_id')
        if level is None:
            level = 0
        if request.user.is_authenticated:
            user= request.user
            new_comment = Comment.objects.create(
                blog_id=blog_id,
                comment=comment,
                user=user,
                level=level,
                parent_id = parent_id if parent_id else None
            )

            data ={
                'id':new_comment.id,
                'comment':new_comment.comment,
                'author_name':user.username,
                'author_id':user.id,
                'level': new_comment.level,
                'parent_id': parent_id
            }
            return JsonResponse({
                'success':True,
                'data':data
            })
        
        return JsonResponse({
            'success':False,
            'error':"Vui long dang nhap"
        })
    
    return JsonResponse({
        'success':False,
        'error':'Invalid request'
    }) 