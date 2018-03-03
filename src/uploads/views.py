from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from uploads.models import Document
from uploads.forms import DocumentForm
from script.main import main as analysis
import os

def home(request):
	documents = Document.objects.all()
	return render(request, 'uploads/home.html', { 'documents': documents })


def simple_upload(request):
	
	if request.method == 'POST' and request.FILES['historico'] and request.FILES['matricula']:
		myfile = request.FILES['historico']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		
		myfile = request.FILES['matricula']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		
		analysis()
		os.system("rm script/base/*.csv; rm script/base/*.xls;")
		return render(request, 'uploads/simple_upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'uploads/simple_upload.html')


def model_form_upload(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('uploads:home')
	else:
		form = DocumentForm()
	return render(request, 'uploads/model_form_upload.html', {
		'form': form
	})
