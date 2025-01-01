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
    path('user_settings/', views.profile_settings, name = 'user_settings')
] 