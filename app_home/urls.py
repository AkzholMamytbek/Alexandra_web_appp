from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('audioblob/', views.get_audio_blob, name='audiofile')
]