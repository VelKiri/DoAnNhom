from django.shortcuts import render

from django.core.paginator import Paginator

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

def blog_list(request):
    blog_list = Blog.objects.all().order_by('-id')
    paginator = Paginator(blog_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog.html',{
        'blog_list': blog_list,
        'page_obj' : page_obj,
        'paginator': paginator,
    })