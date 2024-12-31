from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import RegisterForm, PostForm
from .models import BlogPost


@login_required
def home(request):
    if request.method == 'POST':
        posts = BlogPost.objects.filter(post_name__contains = request.POST.get('search-input'))
    else:
        posts = BlogPost.objects.all()
    return render(request, 'blog/blog_page.html', {'posts' : posts})

@login_required
def post_page(request):
    if request.method == 'POST':
        initial_form = PostForm(request.POST)
        if initial_form.is_valid():
            post_name = initial_form.cleaned_data.get('post_name')
            post_text = initial_form.cleaned_data.get('post_content')
            BlogPost.objects.create(post_name = post_name, post_content = post_text, post_date = timezone.now())
            success_msg = 'Successfully added a blog post!'
    else:
        initial_form = PostForm()
        success_msg = None
    
    return render(request, 'blog/add_post.html', {'form' : initial_form, 'message' : success_msg})

def delete_post(request):
    if request.method == 'POST':
        BlogPost.objects.filter(id = request.POST.get('post_num')).delete()
        return redirect('blog:blog_page')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username = username, password = password)
            # We need the user instance to pass it to the login method. If we only needed to 
            # Insert the form data into a database, we can just call .save() method on the ModelForm instance.
            # If we want to save the changes but not to commit them yet (To modify something later), we can call
            # save(commit = False)
            login(request, user)
            return redirect('blog:blog_page')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form' : form})

def logoutt(request):
    if request.method == 'POST':
        logout(request)
        return redirect('blog:loginn')
    else:
        return redirect('blog:blog_page')

def loginn(request):
    error_msg = None
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'blog:blog_page'
            return redirect(next_url)
        else:
            error_msg = 'Invalid User Credentials!'
    return render(request, 'blog/login_page.html', {'error' : error_msg})