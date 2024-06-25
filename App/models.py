from django.db import models

# Create your models here.
class Book(models.Model):
    author=models.CharField(max_length=50)
    book_name=models.CharField(max_length=100)
    published_date=models.DateField()

    def __str__(self) -> str:
        return self.book_name