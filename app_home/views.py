from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    
    lis = ['apple', 'samsung', 'huawei']





    return render(request, 'app_home/index.html', {'data': lis})

def get_audio_blob(request):
    print(request.status)