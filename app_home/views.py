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

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
media_url = settings.MEDIA_URL

SAMPLE_RATE = 16000
SetLogLevel(0)
model = Model(lang="en")
rec = KaldiRecognizer(model, SAMPLE_RATE)

def ffmpeg(filename):
    print(f"Filename:")
    file_path = os.path.join(media_url, filename)
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                filename,
                                "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE) as process:

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(f"Partial result: {rec.PartialResult()}")
        return rec.FinalResult()

def index(request):
    
    lis = ['apple', 'samsung', 'huawei']
    return render(request, 'app_home/index.html', {'data': lis})

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
        res = ffmpeg(path)
        if res:
             return HttpResponse(res)

        
        return HttpResponse("Не получилось распознать!")
    else:
        pass




        
