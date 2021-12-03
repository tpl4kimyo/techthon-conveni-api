import datetime
from django.utils.timezone import make_aware

from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.db import transaction  # 追加


from webapp.models import PurchaseItemModel, PurchaseModel, StockManageModel
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
        PurchaseItemModel.objects.all().delete()
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
        elif on_sale == "true":
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
            'items':items
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

# /stock/create/multiple
@csrf_exempt
def stock_create_multiple_api(request):

    if request.method == "POST":
        data = JSONParser().parse(request)

        objs = []
        for d in data['items']:
            objs.append(StockManageModel(id=d['id'], name=d['name'],price=d['price'],on_sale=False if d['on_sale'] == "false" else True,count=d['count']))
        
        try:
            StockManageModel.objects.bulk_create(objs)
            return JsonResponse({
                'status_code': 200,
                'method': 'POST'
            })
        except:
            return JsonResponse({
                'status_code': 400,
                'method': 'POST'
            })

# /purchase/detail/{id}
@csrf_exempt
def purchase_detail_api(request, pk):

    if request.method == "GET":
        try:
            purchaseItem = PurchaseItemModel.objects.filter(purchase_id=pk)
        except PurchaseItemModel.DoesNotExist:
            return JsonResponse({
                'status_code': 404,
                'method': 'GET'
            })
        
        items = []
        for item in purchaseItem:
            items.append({
                'stock_id': item.stock_id.id,
                'name': item.stock_id.name,
                'price': item.price,
                'bought_count': item.bought_count
            })

        result = {
            'status_code':200,
            'method':'GET',
            'purchase': {
                'id': pk,
                'bought_at': purchaseItem[0].purchase_id.bought_at.strftime("%Y-%m-%dT%H:%M:%S"),
                'staff_name': purchaseItem[0].purchase_id.staff_name,
                'items': items
            }
        }
        return JsonResponse(result, status=200)

# /purchase/create
@csrf_exempt
def purchase_create_api(request):

    if request.method == "POST":
        data = JSONParser().parse(request)

        with transaction.atomic():
            try:
                purchase = PurchaseModel(id=data['id'], bought_at=make_aware(datetime.datetime.strptime(data['bought_at'], "%Y-%m-%dT%H:%M:%S")), staff_name=data['staff_name'])
                purchase.save()
            except:
                return JsonResponse({
                    'status_code': 400,
                    'method': 'POST'
                })

            for item in data['items']:
                stock = StockManageModel.objects.get(id=item['stock_id'])
                # 在庫計算
                zaiko = stock.count - item['bought_count']
                if zaiko >= 0:
                    stock.count = zaiko
                    stock.save()
                else:
                    return JsonResponse({
                        'status_code': 400,
                        'method': 'POST'
                    })
                
                purchase_item = PurchaseItemModel(purchase_id=purchase, stock_id=stock, price=stock.price, bought_count=item['bought_count'])
                purchase_item.save()
        
        return JsonResponse({
            'status_code': 200,
            'method': 'POST'
        })
