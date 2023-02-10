from django.urls import path
from . import views

app_name = 'rcmd'

urlpatterns = [ 
    path('recommendation', views.recommendation, name="recommendationpage"),
    path('', views.select, name="selectpage"),
    path('results/', views.results, name='resultpage'),
]
