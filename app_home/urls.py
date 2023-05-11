from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/audio-recognizer/', views.get_audio_blob, name='audiofile')
]