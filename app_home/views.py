from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def index(request):
    
    lis = ['apple', 'samsung', 'huawei']
    return render(request, 'app_home/index.html', {'data': lis})

@csrf_exempt
def get_audio_blob(request):
    if request.method == "POST":
        audio_data = request.FILES['audio']
        
        path = default_storage.save('tmp/somename.wav', ContentFile(audio_data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    else:
        pass

# class AudioAPIList(generics.ListCreateAPIView):
#     pass