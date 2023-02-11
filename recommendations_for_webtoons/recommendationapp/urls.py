from django.urls import path
from . import views, views_service, views_static

app_name = 'rcmd'

urlpatterns = [
    path('manage_data', views.manage_data, name="md"),
    
    path('results', views.results, name='resultpage'),
    path('testpage', views.testpage, name='testpage'),
    path('results/', views.results, name='results'),
    
    # ===========================================================
    # ==================       TOP_PAGES        =================
    # ===========================================================
    
    path('servies_test', views_service.service_test, name='service')
    
    
]
