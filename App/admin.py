from django.contrib import admin
from .models import Book
# Register your models here.

@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
    list_display=['id','author','book_name','published_date']