from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import AiciLoginView

app_name="aici"

urlpatterns = [
    path('', AiciLoginView.as_view(template_name='aici/login.html'), name='login'), #로그인페이지
    path('logout/', views.logout_view, name='logout'), 
    path('main/', views.main, name='main'), #메인페이지
    path('main/voc/', views.voc, name='voc'), #voc현황페이지
    path('main/work/', views.work, name='work'), #사외공사
    path('edit_voc/', views.edit_voc, name='edit_voc'), #사외공사
    path('send_mms_proxy/', views.send_mms_proxy, name='send_mms_proxy'),
    path('export1/', views.gongsa_excel, name='gongsa_excel'),
    path('export2/', views.voc_excel, name='voc_excel'),
    # path('update-voc-status/', views.update_voc_status, name='update_voc_status'),

    path('chatbot/', views.chat, name='chatbot'),    
    path('chatbot/<str:phone>/', views.chatbot, name='chat'),
    path('positive/', views.positive, name='positive'),
    path('negative/', views.negative, name='negative'), #메인페이지


]