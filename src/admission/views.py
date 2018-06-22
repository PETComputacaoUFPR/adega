from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages


def upload(request):

    return render(request, 'admission/admission.html')
