from django.shortcuts import render, HttpResponse
from .models import Multiple
import os
from django.conf import settings
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