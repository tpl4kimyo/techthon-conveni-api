from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def check_api(request):

    if request.method == "GET":
        return JsonResponse({
            'status_code': 200,
            'method': 'GET'
        })
    elif request.method == "POST":
        return JsonResponse({
            'status_code': 200,
            'method': 'POST'
        })