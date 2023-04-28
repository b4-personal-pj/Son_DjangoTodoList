from django.db import models
from users.models import User
from datetime import datetime
# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False,blank=True)
    completion_at = models.CharField(max_length=30)

    def __str__(self):
        return str(self.title)

    def complete(self):
        now = datetime.now()
        now = now.strftime("완료 시간 : %Y년 %m월 %d일 %M분")
        self.completion_at = now if self.is_complete else "목표 달성까지 화이팅!"
