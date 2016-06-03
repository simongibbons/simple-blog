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

    def publish(self, publish_date=None):
        """ Publish a post at a specific time, defaults to now """
        if publish_date is None:
            publish_date = timezone.now()
        self.published_date = publish_date
        self.save()

    def unpublish(self):
        """ Clears the published time removing the post from the public site """
        self.published_date = None
        self.save()

    def is_published(self):
        """ Is the post published? """
        return self.published_date is not None

    def is_displayed(self):
        """ Is the post displayable? """
        return self.is_published() and self.published_date <= timezone.now()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog:post_detail', args=[self.pk])

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
