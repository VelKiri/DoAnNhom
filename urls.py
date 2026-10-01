from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.blog_list, name='blog'),
    path('detail/<int:id>/',views.blog_detail,name='blog_detail'),
    path('rate/',views.save_rating,name='save_rating'),
    path('comment/',views.save_comment,name='save_comment'),
]