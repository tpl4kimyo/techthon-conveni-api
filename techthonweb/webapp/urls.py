from django.urls import path, include
from webapp import views

urlpatterns = [
    path('check', views.check_api),
    path('init', views.init_api),
    path('stock/create/single', views.stock_reg_api),
    path('stock/detail/<int:pk>', views.stock_detail_api),
    path('stock/list', views.stock_list_api),
    path('stock/update/<int:pk>', views.stock_update_api),
    path('stock/delete/<int:pk>', views.stock_delete_api),
    path('stock/create/multiple', views.stock_create_multiple_api),
    path('purchase/detail/<int:pk>', views.purchase_detail_api),
    path('purchase/create', views.purchase_create_api),
]
