from django.urls import path
from . import views

app_name = 'coins'

urlpatterns = [
    path('', views.coin_list, name='coin_list'),
    path('<str:coin_name>/<int:coin_id>/', views.coin_detail, name='coin_detail'),
    path('<str:coin_name>/download-csv/', views.download_csv, name='download_csv'),
]
