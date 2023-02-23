from django.urls import path
from . import views, views_service, views_static

app_name = 'rcmd'

urlpatterns = [
    path('manage_data', views.manage_data, name="md"),
    
    path('results', views.results, name='resultpage'),
    path('testpage', views.testpage, name='testpage'),
    path('testpage2', views.testpage2, name='testpage2'),
    path('results/', views.results, name='results'),
    
    # ===========================================================
    # ==================       TOP_PAGES        =================
    # ===========================================================
    
    path('service_test/', views_service.service_test, name='service'),
    path('intro/', views_static.intro, name='intro'),
    path('about/', views_static.about, name='about'),
    
]
