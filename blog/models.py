from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_author_absolute_url(self):
        return reverse('blog:post_list_by_author', kwargs={'author': self.author.id})

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
