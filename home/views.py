from django import template
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')