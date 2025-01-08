from django.db import models
from django.contrib.auth.models import User

def id_values():
    return {'id' : []}

class BlogPost(models.Model):
    id = models.AutoField(primary_key = True)
    post_name = models.CharField(max_length = 60)
    post_content = models.CharField(max_length = 500)
    post_date = models.DateField()
    like_count = models.IntegerField(default = 0)
    dislike_count = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.post_name} - {self.post_content} - {self.post_date}'
    
class UserProfile(models.Model):
    email_address = models.CharField(max_length = 60, null = True)
    phone_number = models.IntegerField(null = True)
    image = models.ImageField(upload_to = 'media/', null = True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    liked_posts = models.JSONField(default = id_values) # The default argument has to be a callable
    disliked_posts = models.JSONField(default = id_values)

class CommentInstances(models.Model):
    associated_user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    associated_post = models.ForeignKey(BlogPost, on_delete = models.CASCADE)
    comment_content = models.CharField(max_length = 500)
    comment_date = models.DateField()