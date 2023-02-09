from django.urls import path
from . import views

#app_name = 'rcmd'

urlpatterns = [
    path('testpage', views.testpage, name='testpage'),
    path('testpage2', views.testpage2, name='testpage2'),
    path('recommendation', views.recommendation, name="recommendationpage"),
    path('', views.selection, name="selectionpage"),

    path('select/', views.select, name='select'),
    path('results/', views.results, name='results'),
]
