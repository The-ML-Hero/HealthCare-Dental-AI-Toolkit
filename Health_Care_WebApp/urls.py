"""Health_Care_WebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import secrets
from WelcomePage.views import welcome
from User_Auth.views import profile_page
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from tooth_fracture_generator.views import regenerate,mode_selection
from flurosis_detector.views import flurosis_detec
from tooth_fracture_detetion.views import fracture_detec
from root_mask_segmentation.views import root_mask

login_url = secrets.token_hex(nbytes=16)
postlogin_url = secrets.token_hex(nbytes=16)
register_user_url = secrets.token_hex(nbytes=32)
encrypted_log = secrets.token_hex(nbytes=64)
tooth_regenerator_url = secrets.token_hex(nbytes=16)
profile_url =  secrets.token_hex(nbytes=16)
flurosis_detector_url = secrets.token_hex(nbytes=16)
fracture_detector_url = secrets.token_hex(nbytes=16)
root_segmentation_url = secrets.token_hex(nbytes=16)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',welcome,name='Welcome-Page'),
    path('accounts/', include('allauth.urls'),name='account_login'),
    path('tooth_regenerator/',regenerate,name='Regenerate'),
    path('profile/',profile_page,name='account_profile'),
    path('modes_regenerate/',mode_selection,name='mode_selection_regenerate_page'),
    path('flurosis_detector/',flurosis_detec,name='flurosis_detection_page'),
    path('fracture_detector/',fracture_detec,name='fracture_detection_page'),
    path('root_segmentation/',root_mask,name='root_segmentation_page'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



