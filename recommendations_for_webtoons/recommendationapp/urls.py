from django.urls import path
from . import views

app_name = 'rcmd'

urlpatterns = [
    path('testpage', views.testpage, name='testpage'),
    path('recommendation', views.recommendation, name="recommendationpage"),
    path('', views.selection, name="selectionpage")
]