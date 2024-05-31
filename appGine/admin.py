from django.contrib import admin
from .models import DataUser,BlockPost,CommentPost

# Register your models here.
admin.site.register(DataUser)
admin.site.register(BlockPost)
admin.site.register(CommentPost)
