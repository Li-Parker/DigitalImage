from django.conf import settings
from django.conf.urls.static import static

from app import views

from django.urls import path

urlpatterns = [
    # path('<str:module>/', app.views.SysView.as_view()),
    path('users/', views.get_users),
    path('login/', views.login),
    path('register/', views.register),
    path('uploadImage/', views.uploadImage),
    path('getImage/', views.get_latest_image),
    path('getUserInfo/', views.get_user_info),
    path('grayImage/', views.gray_image),
    path('clearSession/', views.clear_session),
    path('saveImage/', views.save_image)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
