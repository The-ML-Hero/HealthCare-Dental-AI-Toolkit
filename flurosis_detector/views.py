from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from allauth.account.decorators import login_required,verified_email_required
import os
from .models import Flurosis_Model
import urllib
import numpy as np
import PIL
import requests
from io import BytesIO
import secrets
file_random_name = secrets.token_hex(32)
# Create your views here.


@login_required
def flurosis_detec(request):
    context = {}
    if request.method == 'POST':
        uploaded_file_input = request.FILES.get('flurosis_input_image')
        fs = FileSystemStorage()
        name = fs.save(uploaded_file_input.name, uploaded_file_input)
        context['URL_Input'] = fs.url(name)
        input_image_url = requests.get(f'https://healthcare-toolkit-dental-ai.herokuapp.com{fs.url(name)}')
        Flurosis_Model.objects.create(flurosis_file=uploaded_file_input,flurosis_name='Uploaded File')

        Image_input =  PIL.Image.open(BytesIO(input_image_url.content))
        Image_input.save(f'./Flurosis_Input{file_random_name}.jpg')

        os.system(f"python3 detect.py --weights ./weights/best_flurosis.pt --img 416 --conf 0.5 --source ./Flurosis_Input{file_random_name}.jpg --output ./media/inference/output/")
        Flurosis_Model.objects.create(flurosis_image =f'./inference/output/Flurosis_Input{file_random_name}.jpg' ,flurosis_name='Output File')
        context['URL_Output'] = f'https://healthcare-toolkit-dental-ai.herokuapp.com/media/inference/output/Flurosis_Input{file_random_name}.jpg'

    return render(request,'flurosis.html',context)
