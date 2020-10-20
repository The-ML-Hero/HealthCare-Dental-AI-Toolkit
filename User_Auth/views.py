from django.shortcuts import render

def profile_page(requests):
    return render(requests,'profile.html')