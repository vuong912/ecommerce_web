from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
register = template.Library()
def index(request):
    return render(request, 'home/index.html')