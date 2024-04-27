from django.shortcuts import render, HttpResponse, redirect
from .models import Multiple
import os
from django.conf import settings
from django.http import JsonResponse
import google.generativeai as genai
from gtts import gTTS
from pyresparser import ResumeParser as repr
# Create your views here.

similarity_scores=[0.0]*3
position=""

def index(request):
    if request.method == "GET":
        return render(request , 'IntervueApp/index.html')
    if request.method == "POST":
        position = request.POST.get('position') 
        return redirect(upload)
    
    
def upload(request):
    if request.method == 'POST':
        files=request.FILES.getlist('files')
        print(files)
        for uploaded_file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        process_media_folder()   
        return redirect()
      
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
        return render(request, 'IntervueApp/play_audio.html')

def process_media_folder():
    media_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
    
    if not os.path.exists(media_folder):
        print("Media folder does not exist.")
        return
    
    files = os.listdir(media_folder)
    
    pdf_files = [file for file in files if file.endswith('.pdf')]
    if pdf_files:
        print("PDF files found in the media folder:")
        for pdf_file in pdf_files:
            print("- " + pdf_file)
        process_pdf_files(pdf_files)
    
    img_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if img_files:
        print("Image files found in the media folder:")
        for img_file in img_files:
            print("- " + img_file)
        process_image_files(img_files)

def process_pdf_files(pdf_files):
    data = repr(pdf_files[0]).get_extracted_data()
    name = data['name']
    skills= data['skills']

def process_image_files(img_files):
    print("Processing image files...")
