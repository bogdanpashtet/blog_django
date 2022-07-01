from django.shortcuts import render
from django.http import HttpResponse
from .models import Articles


def index(request):
    return render(request, 'blog/index.html')


def profile(request):
    return HttpResponse('<h1>This is a profile page</h1>')
