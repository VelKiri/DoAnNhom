from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.blog_list, name='Blog'),
    path("search/", views.search_view, name="search"),
    path("search-advanced/",views.search_advanced_view,name="search_advanced"),
    path("ajax-search-advanced/",views.ajax_search_advanced_view,name="ajax_search_advanced"),
    path('detail/<int:id>/', views.blog_detail, name='blog_detail'),
    path('rate/',views.save_rating,name='save_rating'),
    path('comment/',views.save_comment,name='save_comment'),

]