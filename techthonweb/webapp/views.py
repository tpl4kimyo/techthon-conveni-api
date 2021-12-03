from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.db.models import Q



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

# /stock/list
@csrf_exempt
def stock_list_api(request):

    if request.method == "GET":
        min_count = request.GET.get('min_count')
        max_count = request.GET.get('max_count')
        on_sale = request.GET.get('on_sale')

        min_count_q = Q()
        max_count_q = Q()
        on_sale_q = Q()
        if min_count:
            min_count_q = Q(count__gte=min_count)
        if max_count:
            max_count_q = Q(count__lte=max_count)
        if on_sale == "false":
            on_sale_q = Q(on_sale=False)
        else:
            on_sale_q = Q(on_sale=True)
        
        stocks = StockManageModel.objects.filter(min_count_q & max_count_q & on_sale_q)
        items = []
        for stock in stocks:
            item = {
                'id':stock.id,
                'name':stock.name,
                'price':stock.price,
                'on_sale':stock.on_sale,
                'count':stock.count
            }

            items.append(item)
        
        result = {
            'status_code':200,
            'method':'GET',
            'item':items
        }

        return JsonResponse(result)

@csrf_exempt
def stock_update_api(request, pk):

    if request.method == "PUT":
        try:
            stock = StockManageModel.objects.get(id=pk)
        except StockManageModel.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'method': 'PUT'
            })
        
        data = JSONParser().parse(request)
        if 'name' in data:
            stock.name = data['name']
        if 'price' in data:
            stock.price = data['price']
        if 'on_sale' in data:
            stock.on_sale = False if data['on_sale'] == "false" else True
        if 'count' in data:
            stock.count = data['count']
        
        stock.save()
        
        result = {
            'status_code':200,
            'method':'PUT',
        }
        return JsonResponse(result, status=200)

@csrf_exempt
def stock_delete_api(request, pk):

    if request.method == "DELETE":
        try:
            stock = StockManageModel.objects.get(id=pk)
        except StockManageModel.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'method': 'DELETE'
            })
        
        stock.delete()
        
        result = {
            'status_code':200,
            'method':'DELETE',
        }
        return JsonResponse(result, status=200)



class StockManageViewSet(viewsets.ModelViewSet):
    queryset = StockManageModel.objects.all()
    serializer_class = StockManageSerializer
