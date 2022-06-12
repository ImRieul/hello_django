from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Model를 수정했을 땐 makemigrations, migrate를 통헤 DB를 변경해주어야 한다. https://wikidocs.net/71306


class Question(models.Model):
    # 멤버 변수 = 변수 타입
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # on_delete=models.CASCDE -> Question이 삭제될 경우 Answer도 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)