from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    """ Data model for a blog post """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    text = models.TextField()

    creation_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
