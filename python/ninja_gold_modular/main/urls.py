from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('reset', views.reset),#reset the game
    path('process', views.process_money),# post request version of process money
    path('<location>', views.process_money),# get request version of process money
]