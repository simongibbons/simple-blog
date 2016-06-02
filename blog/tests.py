import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Post


class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user")

    def create_post(self):
        post = Post()
        post.author = self.user
        post.title = "Test Post"
        post.save()
        post.refresh_from_db()
        return post

    def test_post_defaults_unpublished(self):
        post = self.create_post()
        assert post.published_date is None

    def test_publish_now(self):
        post = self.create_post()
        post.publish()

        assert post.is_published()
        assert post.is_displayed()

    def test_publish_in_past(self):
        post = self.create_post()

        publish_date = timezone.now() - datetime.timedelta(days=1)
        post.publish(publish_date)
        post.refresh_from_db()

        assert post.is_published()
        assert post.is_displayed()
        assert post.published_date == publish_date

    def test_publish_in_future(self):
        post = self.create_post()

        publish_date = timezone.now() + datetime.timedelta(days=1)
        post.publish(publish_date)

        assert post.is_published()
        assert not post.is_displayed()
        assert post.published_date == publish_date

    def test_unpublishing_a_post(self):
        post = self.create_post()
        post.publish()
        post.refresh_from_db()

        assert post.is_published()

        post.unpublish()
        post.refresh_from_db()

        assert not post.is_published()
        assert not post.is_displayed()

