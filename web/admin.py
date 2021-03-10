from django.contrib import admin

from .models import Post, Comment, CommentLikes

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentLikes)

