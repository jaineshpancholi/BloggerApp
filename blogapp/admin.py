from django.contrib import admin
from blogapp.models import *

# Register your models here.

admin.site.register(UserDetail)
admin.site.register(Category)
admin.site.register(BlogModel)
admin.site.register(LikeBlog)
admin.site.register(CommentBLog)


