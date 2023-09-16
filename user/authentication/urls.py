from django.urls import path, include
from . import views
from django.contrib import admin
from authentication.views import signin, signup, signout, index, home, upload_file, myupload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('index', views.index, name="index"),
    path('myupload', views.myupload, name="myupload"),
    path('upload_file', views.upload_file, name="upload_file"),
    path('inbox/', views.inbox, name='inbox'), 
    path('list/', views.upload_file, name="list"),
    path('student/', views.StudentView.as_view(), name='student'),
    path('delete/<int:pk>/', views.delete_file, name='delete_file'),
    path('message/view/<int:message_id>/', views.view_message, name='view_message'),
    path('view_inbox/', views.inbox, name='view_inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('compose/', views.compose_message, name='compose_message'),
    path('delete/message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('sent/<int:message_id>/', views.view_sent_message, name='view_sent_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)