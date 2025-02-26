from . import views
from django.urls import path

urlpatterns=[
    path('', views.index, name='index'),
    path('blog-details/featured', views.featured, name='featured'),
    path('blog-details/<str:pk>', views.details, name='details'),
    path('author-profile/', views.author, name='author'),
    path('contact/', views.contacts, name='contacts')
]