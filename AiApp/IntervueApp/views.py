from django.shortcuts import render, HttpResponse, redirect
from .models import Multiple
import os
from django.conf import settings
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request , 'IntervueApp/index.html')

def upload(request):
    if request.method == 'POST':
        files=request.FILES.getlist('files')
        print(files)
        # for uploaded_file in files:
        #     file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        #     os.makedirs(os.path.dirname(file_path), exist_ok=True)
        #     with open(file_path, 'wb') as destination:
        #         for chunk in uploaded_file.chunks():
        #             destination.write(chunk)
                    
    return render(request, 'IntervueApp/upload.html')

def record_and_process_audio(request):
    if request.method == 'GET':
        return render(request, 'IntervueApp/record_audio.html')
    elif request.method == 'POST':
        if request.FILES.get('audio'):
            audio_file = request.FILES['audio']
            os.makedirs(os.path.dirname(settings.MEDIA_ROOT + '\\audio\\audio.wav'), exist_ok=True)
            with open(settings.MEDIA_ROOT + '\\audio\\audio.wav', 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            return redirect(play_audio)
        else:
            return JsonResponse({'status': 'error', 'message': 'No audio file found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported request method'})
    
    
def play_audio(request):
    if request.method == "GET":
        return render(request, 'IntervueApp/play_audio.html')
