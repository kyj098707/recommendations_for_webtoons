from django.urls import path
from . import views, views_service, views_static, views_account

app_name = 'rcmd'

urlpatterns = [
    path('manage_data', views.manage_data, name="md"),
    path('testpage', views.testpage, name='testpage'),
    
    # ===========================================================
    # ==================       TOP_PAGES        =================
    # ===========================================================
    
    path('search/', views_service.service_artwork, name='search'),
    path('search/<str:keyword>', views_service.service_artwork, name='search_result'),
    
    path('service/', views_service.main, name='service'),
    path('service/artwork/<str:artwork_id>/', views_service.service_artwork, name='service_artwork'),
    
    
    
    path('intro/', views_static.intro, name='intro'),
    
    path('about/', views_static.about, name='about'),
    
    # ===========================================================
    # ==================       Account_PAGES        =================
    # ===========================================================
    
    path('auth00/', views_account.join, name='join'),
    path('auth01/', views_account.log_in, name='log_in'),
    path('logout/', views_account.logout, name='logout'),
    # path('account/', views_account.log_out, name='account'),
    
    # path('account/', views_account.account_test, name='account'),
    path('sendemail/', views_account.sendemail, name='send_mail'),
#    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid>/<str:token>/', views_account.activate, name='activate'),

    
]
