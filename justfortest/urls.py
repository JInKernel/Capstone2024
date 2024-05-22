from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('under60/', views.under60, name='under60'),
    path('over60/', views.over60, name='over60'),
    path('get-prediction/', views.get_prediction, name='get-prediction')
]