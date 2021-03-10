from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Likes(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')


class Dislikes(models.Model):
    post = models.ForeignKey(Post, related_name='dislikes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='dislikes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')


class CommentDislikes(models.Model):
    comment = models.ForeignKey(Comment, related_name='comment_dislikes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_dislikes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')


class CommentLikes(models.Model):
    comment = models.ForeignKey(Comment, related_name='comment_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')
