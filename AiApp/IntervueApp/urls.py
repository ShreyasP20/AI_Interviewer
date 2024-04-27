from django.urls import path
from IntervueApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('record_and_process_audio/', views.record_and_process_audio, name='record_and_process_audio'),
    path('play_audio', views.play_audio, name='play_audio'),
    path('upload', views.upload, name='upload')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
