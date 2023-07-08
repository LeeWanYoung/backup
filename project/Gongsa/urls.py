from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import GongsaLoginView


app_name="gongsa"

urlpatterns = [
    path('', GongsaLoginView.as_view(template_name='gongsa/gongsalogin.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main, name='main'), #메인페이지
    path('upload/', views.upload, name='upload'), #사외공사접수
    path('worklist/', views.worklist, name='worklist'), #사외공사목록
    path('update/<int:post_id>/', views.update, name='update'),  # 사외공사접수수정

]