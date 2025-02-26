from django.shortcuts import render
from .models import Post

def index(request):
    posts=Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def author(request):
    return render(request, 'author-profile.html')


def featured(request):
    return render(request, 'featured-blog-details.html')


def details(request, pk):
    posts=Post.objects.get(id=pk)
    return render(request, 'blog-details.html', {'posts': posts})


def contacts(request):
    return render(request, 'contact.html')


def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)
