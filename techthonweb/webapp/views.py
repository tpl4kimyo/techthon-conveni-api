from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


from webapp.models import StockManageModel
from webapp.serializers import StockManageSerializer

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

@csrf_exempt
def init_api(request):

    if request.method == "PUT":

        StockManageModel.objects.all().delete()
        smm = StockManageModel(id = 1, name = 'pen', price = 100, on_sale = True, count = 100)
        smm.save()

        return JsonResponse({
            'status_code': 200,
            'method': 'PUT'
        })

@csrf_exempt
def stock_reg_api(request):

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = StockManageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status_code': 201,
                'method': 'POST'
            })
        else:
            return JsonResponse({
                'status_code': 400,
                'method': 'POST'
            })

@csrf_exempt
def stock_detail_api(request, pk):

    if request.method == "GET":
        try:
            stock = StockManageModel.objects.get(id=pk)
        except StockManageModel.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'method': 'GET'
            })
        
        result = {
            'status_code':200,
            'method':'GET',
            'item':{
                'id':stock.id,
                'name':stock.name,
                'price':stock.price,
                'on_sale':stock.on_sale,
                'count':stock.count
            }
        }
        return JsonResponse(result, status=200)

class StockManageViewSet(viewsets.ModelViewSet):
    queryset = StockManageModel.objects.all()
    serializer_class = StockManageSerializer
