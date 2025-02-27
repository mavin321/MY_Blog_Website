from django.shortcuts import render
from .models import Post
import markdown
from django.utils.safestring import mark_safe

def index(request):
    posts=Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def author(request):
    return render(request, 'author-profile.html')


def featured(request):
    return render(request, 'featured-blog-details.html')


def details(request, pk):
    posts=Post.objects.get(id=pk)
    posts.content = mark_safe(markdown.markdown(posts.content, extensions=["fenced_code", "tables", "toc"]))
    return render(request, 'blog-details.html', {'posts': posts})


def contacts(request):
    return render(request, 'contact.html')


def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)
