from django.contrib import admin

# Register your models here.
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Blog, BlogAdmin)
