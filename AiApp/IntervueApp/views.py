from django.shortcuts import render, HttpResponse, redirect
from .models import Multiple
import os
from django.conf import settings
from django.http import JsonResponse
import google.generativeai as genai
from gtts import gTTS
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pypdf
from PIL import Image
from IPython.display import Markdown
import textwrap
from django.views.decorators.csrf import csrf_exempt
import API_KEY
# Create your views here.

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "max_output_tokens": 8192,
}
similarity_scores=[]
resume=""
position = ""
answer=""
follow_up_q=False
model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key=API_KEY.API_KEY)
chat=model.start_chat(history=[])
current_answer=""
current_question=""
fu_question=""


def speak(text):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, 'audio', 'question.mp3'))
    except:
        pass
    tts = gTTS(text=text, lang='en', slow=False, tld='com', lang_check=False)
    audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', 'question.mp3')
    tts.save(audio_path)


def to_markdown(text):
    text = text.replace('•', '  *')
    return str(Markdown(textwrap.indent(text, '> ', predicate=lambda _: True)))


def index(request):
    global position
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
        return redirect(play_audio)
    return render(request, 'IntervueApp/upload.html')


@csrf_exempt  
def process_text(request):
    if request.method == 'GET':
        return render(request, 'IntervueApp/record_and_process.html')

    elif request.method == 'POST':
        text = request.POST.get('text', '')  
        print("Received text:", text)
        current_answer = text 
        if current_answer == "NAN":
            return JsonResponse({'status': 'error', 'message': 'No Audio Recorded '})
        response = chat.send_message(f"Give an ideal answer, for the question {current_question} considering the skills {resume}")
        ideal_nu_answer= response.text.replace('\n', '').replace('```', '') 
        tokens1 = set(word_tokenize(current_answer.lower())) - set(stopwords.words('english'))
        tokens2 = set(word_tokenize(ideal_nu_answer.lower())) - set(stopwords.words('english'))
        similarity_score = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))
        if similarity_score < 50:
            follow_up_q = True
        else:
            follow_up_q = False
        similarity_scores.append(similarity_score)
        return redirect(play_audio)
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported request method'})



def play_audio(request):
    resume = process_media_folder()
    if follow_up_q:
        response = chat.send_message(f"Ask a follow up question for {position} in a company. the resume of the person is:{resume},reviewing the previous answer")
        fu_question = response.text.replace('\n', '').replace('```', '')
        speak(fu_question)
        return render(request, 'IntervueApp/play_audio.html')
    else:
        try:
            response = chat.send_message(f"You are a recruiter at a Company, ask one question for {position} in a company based on the skills make that question technical. the resume of the person is: {resume}")       
            current_question = response.text.replace('\n', '').replace('```', '')
        except:
            current_question = " What is your experience with Python?"
        speak(current_question)
        return render(request, 'IntervueApp/play_audio.html')



def process_media_folder():
    data = ""
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
        data = process_pdf_files(pdf_files)
    img_files = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if img_files:
        print("Image files found in the media folder:")
        for img_file in img_files:
            print("- " + img_file)
        data = process_image_files(img_files)
    return str(data)

def process_pdf_files(pdf_files):
    print("REACHED")
    for pdf_file in pdf_files:
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file)

        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(pdf_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text


def process_image_files(img_files):
    model = genai.GenerativeModel('gemini-pro-vision')
    text=""
    for img_file in img_files:
        img_path = os.path.join(settings.MEDIA_ROOT, img_file)
        img = Image.open(img_path)
        response = model.generate_content(['What do u see?',img], stream=True)
        response.resolve()
        new_text = to_markdown(response.text)
        text = text + new_text

    resume=text
    print(resume)
    print("Processing image files...")
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

def result(request):
    try:
        final_score = sum(similarity_scores)/len(similarity_scores)
    except:
        final_score=0
    context = {'final_score': final_score}
    return render(request, 'IntervueApp/result.html', context)