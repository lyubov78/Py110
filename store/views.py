from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart

# Create your views here.

def products_view(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if id:
            if id in DATABASE:
                return JsonResponse(DATABASE[id], json_dumps_params={'indent': 4, 'ensure_ascii': False})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        category_key = request.GET.get("category")
        ordering_key = request.GET.get("ordering")
        if category_key:
            if ordering_key:
                if request.GET.get("reverse") in ('true', 'True'):
                    data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
                    return JsonResponse(data, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})
                else:
                    data = filtering_category(DATABASE, category_key, ordering_key)
                    return JsonResponse(data, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})

            data = filtering_category(DATABASE, category_key)
            return JsonResponse(data, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})

    return JsonResponse(DATABASE, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', 'r', encoding="utf-8") as f:
                        data = f.read()
                        return HttpResponse(data)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', 'r', encoding="utf-8") as f:
                    data = f.read()
                    return HttpResponse(data)
        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})