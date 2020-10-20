from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import PIL
from PIL import Image
import os
from .models import Document
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.decorators import login_required,verified_email_required
import cv2
import urllib
import numpy as np
import secrets
# Create your views here.

random_file_name = secrets.token_hex(32)

@login_required
def regenerate(request):
    context = {}
    if request.method == 'POST':
        uploaded_file_input = request.FILES.get('document_input_image')
        uploaded_file_mask = request.FILES.get('document_input_mask')
        slider_value = request.POST.getlist('inpainting_value')
        fs = FileSystemStorage()
        name = fs.save(uploaded_file_input.name, uploaded_file_input)
        name_mask  = fs.save(uploaded_file_mask.name, uploaded_file_mask)
        context['URL_Input'] = fs.url(name)
        context['URL_Mask'] = fs.url(name_mask)
        Document.objects.create(document=uploaded_file_input,document_name='Uploaded File')
        Document.objects.create(document=uploaded_file_mask,document_name='Uploaded File Mask')
        image_input = urllib.request.urlopen(f'http://127.0.0.1:1234{fs.url(name)}')
        mask_input = urllib.request.urlopen(f'http://127.0.0.1:1234{fs.url(name_mask)}')
        arr_input = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
        arr_mask = np.asarray(bytearray(mask_input.read()), dtype=np.uint8)

        Image_input =  cv2.imdecode(arr_input, -1)
        Image_mask = cv2.imdecode(arr_mask, -1)
        Image_mask = cv2.cvtColor(Image_mask, cv2.COLOR_BGR2GRAY)
        output = cv2.inpaint(Image_input, Image_mask,int(slider_value[0]), cv2.INPAINT_TELEA)
        cv2.imwrite(f'{str(settings.MEDIA_ROOT)}/Output_CV2_MASK.png{random_file_name}.png',output)
        Document.objects.create(document_image =f'/Output_CV2_MASK.png{random_file_name}.png' ,document_name='Output File')
        context['URL_Output'] = f'http://127.0.0.1:1234/media/Output_CV2_MASK.png{random_file_name}.png'
    return render(request,'toothregenerator.html',context)    

@login_required
def mode_selection(request):
    return render(request,'modes.html')