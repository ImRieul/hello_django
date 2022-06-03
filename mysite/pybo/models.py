from django.db import models

# Create your models here.


class Question(models.Model):
    # 멤버 변수 = 변수 타입
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # on_delete=models.CASCDE -> Question이 삭제될 경우 Answer도 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()