from django.shortcuts import render,HttpResponse
from .models import Book
# Create your views here.

def home(request):
    books=Book.objects.all()
    return render(request,'index.html',{'Books':books})