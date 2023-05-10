from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel
from app_home.transcriber import Transcriber
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
media_url = settings.MEDIA_URL

transcriber = Transcriber()


def transcribe(filename):
    filepath = os.path.abspath(filename)
    transcription = transcriber.transcribe(filepath)

    print(transcription)

def index(request):
    return render(request, 'app_home/index.html')

@csrf_exempt
def get_audio_blob(request):
    if request.method == "POST":
        audio_data = request.FILES['audio']
        
        path = default_storage.save(os.path.join('audio', 'somename.wav'), ContentFile(audio_data.read()))
        
        
        with open(os.path.join('file.wav'), 'wb') as f:
            f.write(audio_data.read())

        # with open(os.path.abspath(path), 'wb') as f:
        #     f.write(file.stream._file.read())
        # tmp_file = os.path.join('file.wav')
        
        res = transcribe(path)
        if res:
             return HttpResponse(res)

        
        return HttpResponse("Не получилось распознать!")
    else:
        pass




        
