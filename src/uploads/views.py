from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from uploads.models import Submission

from uploads.core.models import Document
from uploads.core.forms import DocumentForm



def home(request):
    documents = Document.objects.all()
    return render(request, 'uploads/home.html', {'documents': documents})



def simple_upload(request):
    if request.method == 'POST' and request.FILES['historico'] and request.FILES['matricula']:

        submission = Submission.objects.create(author=request.user)
        submission.course = '21A'

        fs = FileSystemStorage(location=submission.path())

        fs.save('historico.xls', request.FILES['historico'])
        fs.save('matricula.xls', request.FILES['matricula'])

        submission.historico.name = submission.path() + '/historico.xls'
        submission.matricula.name = submission.path() + '/matricula.xls'

        submission.save()

    return render(request, 'core/simple_upload.html')


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
