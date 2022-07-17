from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, SubsUser
from testytest.models import Product


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(SubsUser)
admin.site.register(Product)