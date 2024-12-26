from django.db import models

class BlogPost(models.Model):
    id = models.IntegerField(primary_key = True)
    post_name = models.CharField(max_length = 60)
    post_content = models.CharField(max_length = 500)
    post_date = models.DateField()

    def __str__(self):
        return f'{self.post_name} - {self.post_content} - {self.post_date}'
    
