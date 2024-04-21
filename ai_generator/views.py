from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import BlogPost

# Create your views here.
@login_required
def index(request):
    return render(request, 'ai_generator/index.html', {})

@login_required
def all_blogs(request):
    return render(request, 'ai_generator/blogs.html')

@login_required
def single_blog(request, id):
    blog = BlogPost.objects.get(id=id)

    if blog is None:
        return redirect('home')
    
    return render(request, 'ai_generator/single.html', {'blog':blog})