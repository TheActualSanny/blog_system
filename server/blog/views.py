from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import F
from .forms import RegisterForm, PostForm, ProfileForm
from .models import BlogPost, UserProfile, CommentInstances

@login_required
def home(request):
    try:
        profile_image = UserProfile.objects.get(user__id = request.user.id)
    except UserProfile.DoesNotExist:
        profile_image = None
    if request.method == 'POST':
        posts = BlogPost.objects.filter(post_name__contains = request.POST.get('search-input'))
    else:
        posts = BlogPost.objects.all()
    return render(request, 'blog/blog_page.html', {'posts' : posts, 'profile' : profile_image})

@login_required
def detailed_post(request, post_id):
    selected_post = BlogPost.objects.get(pk = post_id)
    comment_section = CommentInstances.objects.filter(associated_post__id = selected_post.id)
    return render(request, 'blog/detailed_blog.html', {'post' : selected_post, 'comments' : comment_section})

@login_required
def add_comment(request):
    if request.method == 'POST':
        current_profile = UserProfile.objects.get(user__id = request.user.id)
        associated_post = BlogPost.objects.get(pk = request.POST.get('post-id'))
        try:
            CommentInstances.objects.create(associated_user = current_profile, associated_post = associated_post, 
                            comment_content = request.POST.get('comment-content'), comment_date = timezone.now())
        except Exception as error:
            print(error)
    return redirect('blog:detailed_post', post_id = int(request.POST.get('post-id')))

def post_page(request):
    if request.method == 'POST':
        initial_form = PostForm(request.POST)
        if initial_form.is_valid():
            post_name = initial_form.cleaned_data.get('post_name')
            post_text = initial_form.cleaned_data.get('post_content')
            BlogPost.objects.create(like_count = 0, dislike_count = 0, post_name = post_name, 
                                    post_content = post_text, post_date = timezone.now())
            success_msg = 'Successfully added a blog post!'
    else:
        initial_form = PostForm()
        success_msg = None
    
    return render(request, 'blog/add_post.html', {'form' : initial_form, 'message' : success_msg})

@login_required
def like_post(request):
    if request.method == 'POST':
        current_post = request.POST.get('post-id')
        post = BlogPost.objects.filter(pk = current_post)
        liked = UserProfile.objects.get(user__id = request.user.id)
        if current_post in liked.liked_posts['id']:
            post.update(like_count = F('like_count') - 1)
            liked.liked_posts['id'].remove(current_post)
            liked.save()
        else:
            post.update(like_count = F('like_count') + 1)
            liked.liked_posts['id'].append(current_post)
            liked.save()
    return redirect('blog:blog_page')

@login_required
def dislike_post(request):
    if request.method == 'POST':
        current_post = request.POST.get('post-id')
        post = BlogPost.objects.filter(pk = current_post)
        disliked = UserProfile.objects.get(user__id = request.user.id)
        if current_post in disliked.disliked_posts['id']:
            post.update(dislike_count = F('dislike_count') - 1)
            disliked.disliked_posts['id'].remove(current_post)
            disliked.save()
        else:
            post.update(dislike_count = F('dislike_count') + 1)
            disliked.disliked_posts['id'].append(current_post)
            disliked.save()
    return redirect('blog:blog_page')

@login_required
def profile_settings(request):
    if request.method == 'POST':
        changed_profile = ProfileForm(request.POST, request.FILES)
        if changed_profile.is_valid():
            new_email = changed_profile.cleaned_data.get('email_address')
            new_phone = changed_profile.cleaned_data.get('phone_number')
            new_image = changed_profile.cleaned_data.get('image')
            try:
                UserProfile.objects.create(email_address = new_email, phone_number = new_phone,
                                           image = new_image, user = request.user)
            except IntegrityError:
                UserProfile.objects.filter(user__id = request.user.id).update(email_address = new_email, phone_number = new_phone,
                                           image = new_image)
            success_msg = "Successfully changed profile settings!"
    else:
        changed_profile = ProfileForm()
        success_msg = None
    
    return render(request, 'blog/user_settings.html', {'profile' : changed_profile, 'message' : success_msg})
            
@login_required
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
            UserProfile.objects.create(image = None, phone_number = None, email_address = None, user = user)
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