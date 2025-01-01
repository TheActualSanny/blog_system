from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    id = models.AutoField(primary_key = True)
    post_name = models.CharField(max_length = 60)
    post_content = models.CharField(max_length = 500)
    post_date = models.DateField()

    def __str__(self):
        return f'{self.post_name} - {self.post_content} - {self.post_date}'
    
class UserProfile(models.Model):
    email_address = models.CharField(max_length = 60)
    phone_number = models.IntegerField()
    image = models.ImageField(upload_to = 'media/')
    user = models.OneToOneField(User, on_delete = models.CASCADE)
