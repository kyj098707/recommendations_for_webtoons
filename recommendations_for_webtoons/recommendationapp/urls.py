from django.urls import path
from . import views

app_name = 'rcmd'

urlpatterns = [ 
    path('recommendation', views.recommendation, name="recommendationpage"),
    path('', views.select, name="selectpage"),
    path('results', views.results, name='resultpage'),
    path('testpage', views.testpage, name='testpage'),
    path('testpage2', views.testpage2, name='testpage2'),
]
