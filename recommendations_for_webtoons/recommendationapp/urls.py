from django.urls import path
from . import views, views_service, views_static, views_account

app_name = 'rcmd'

urlpatterns = [
    path('manage_data', views.manage_data, name="md"),
    path('testpage', views.testpage, name='testpage'),
    
    # ===========================================================
    # ==================       TOP_PAGES        =================
    # ===========================================================
    
    path('service_test/', views_service.service_test, name='service'),
    path('intro/', views_static.intro, name='intro'),
    path('about/', views_static.about, name='about'),
    
    # ===========================================================
    # ==================       Account_PAGES        =================
    # ===========================================================
    
    path('auth00/', views_account.join, name='join'),
    path('auth01/', views_account.log_in, name='log_in'),
    # path('account/', views_account.log_out, name='account'),
    
    path('account/', views_account.account_test, name='account'),
    path('logout/', views_account.logout_test, name='logout'),
    path('', views_account.push_btn, name='push_btn'),
    path('sendemail/', views_account.sendemail, name='send_mail'),
#    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid>/<str:token>/', views_account.activate, name='activate'),

    
]
