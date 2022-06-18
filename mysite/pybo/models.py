from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Model를 수정했을 땐 makemigrations, migrate를 통헤 DB를 변경해주어야 한다. https://wikidocs.net/71306


class Question(models.Model):
    # 멤버 변수 = 변수 타입
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    modify_date = models.DateTimeField(null=True, blank=True)  # null 허용, form.is_valid 검증 시 값 없어도 됨(값을 비워둘 수 있음)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가

    def __str__(self):
        return self.subject


class Answer(models.Model):
    # on_delete=models.CASCDE -> Question이 삭제될 경우 Answer도 삭제됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    modify_date = models.DateTimeField(null=True, blank=True)  # null 허용, form.is_valid 검증 시 값 없어도 됨(값을 비워둘 수 있음)
    voter = models.ManyToManyField(User, related_name='voter_answer')  # 추천인 추가

    # related_name : 연결된 테이블(author, voter)을 구분해줌
