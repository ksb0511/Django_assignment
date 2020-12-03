import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # __str__ 메소드를 추가한 이유) 객체의 표현을 대화식 프롬프트로 볼 용도 + 관리사이트에서도 객체의 표현이 사용되기 때문
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # __str__ 메소드를 추가한 이유) 객체의 표현을 대화식 프롬프트로 볼 용도 + 관리사이트에서도 객체의 표현이 사용되기 때문
    def __str__(self):
        return self.choice_text
