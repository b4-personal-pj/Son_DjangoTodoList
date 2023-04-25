from django.db import models
from users.models import User
# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)