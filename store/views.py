from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .models import DATABASE

# Create your views here.

def products_view(request):
    if request.method == "GET":
        return JsonResponse(DATABASE, json_dumps_params={'indent': 4, 'ensure_ascii': False})


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)