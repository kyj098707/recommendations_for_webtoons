from django.urls import path
from . import views

app_name = 'rcmd'

urlpatterns = [
    path('testpage', views.testpage, name='testpage'),
    path('', views.home, name="recommendations-home")
]   