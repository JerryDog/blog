from django.contrib import admin

from online.models import Blogs, Comments, IndexViews, PhotoViews

# Register your models here.

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(IndexViews)
admin.site.register(PhotoViews)
