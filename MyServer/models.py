import datetime

from django.db import models
from django.utils import timezone


# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class WhiteList(models.Model):
    app_name = models.CharField(max_length=256)
    version = models.CharField(max_length=256)
    ip_addr = models.CharField(max_length=256)

    class Meta:
        unique_together = ("app_name", "version", "ip_addr")


class UnauthorizedApp(models.Model):
    app_name = models.CharField(max_length=256)
    reason = models.CharField(max_length=256)  # app reason / version reason
    ip_addr = models.CharField(max_length=256)
    install_date = models.CharField(max_length=256)  # datekey format YYYYMMDD

    class Meta:
        unique_together = ("app_name", "ip_addr")


