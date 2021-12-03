from django.urls import path, include
from webapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stock', views.StockManageViewSet)

urlpatterns = [
    path('check', views.check_api),
    path('init', views.init_api),
    path('stock/create/single', views.stock_reg_api),
    path('stock/detail/<int:pk>', views.stock_detail_api),
    path('', include(router.urls)),
]
