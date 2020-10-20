from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from allauth.account.decorators import login_required,verified_email_required
import os
from .models import Fracture_Model
import urllib
import numpy as np
import PIL
import requests
from io import BytesIO
import secrets
file_random_name = secrets.token_hex(35)
# Create your views here.

@login_required
def fracture_detec(request):
    context = {}
    if request.method == 'POST':
        uploaded_file_input = request.FILES.get('fracture_input_image')
        fs = FileSystemStorage()
        name = fs.save(uploaded_file_input.name, uploaded_file_input)
        context['URL_Input'] = fs.url(name)
        input_image_url = requests.get(f'https://healthcare-toolkit-dental-ai.herokuapp.com{fs.url(name)}')
        Fracture_Model.objects.create(fracture_file=uploaded_file_input,fracture_name='Uploaded File')

        Image_input =  PIL.Image.open(BytesIO(input_image_url.content))
        Image_input.save(f'Fracture_Input{file_random_name}.jpg')

        os.system(f"python3 detect.py --weights ./weights/best.pt --img 416 --conf 0.5 --source Fracture_Input{file_random_name}.jpg --output ./media/inference/output/")
        Fracture_Model.objects.create(fracture_image =f'./media/inference/output/Fracture_Input{file_random_name}.jpg' ,fracture_name='Output File')
        context['URL_Output'] = f'https://healthcare-toolkit-dental-ai.herokuapp.com/media/inference/output/Fracture_Input{file_random_name}.jpg'

    return render(request,'fracture.html',context)
