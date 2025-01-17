from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.loginn, name = 'loginn'),
    path('logout/', views.logoutt, name = 'logoutt'),
    path('register/', views.register, name = 'register'),
    path('blog/', views.home, name = 'blog_page'),
    path('blog_post/', views.post_page, name = 'post_page'),
    path('delete_post/', views.delete_post, name = 'delete_post'),
    path('user_settings/', views.profile_settings, name = 'user_settings'),
    path('like_post/', views.like_post, name = 'like_post'),
    path('dislike_post/', views.dislike_post, name = 'dislike_post'),
    path('post/<int:post_id>', views.detailed_post, name = 'detailed_post'),
    path('add_comment/', views.add_comment, name = 'add_comment')
] 