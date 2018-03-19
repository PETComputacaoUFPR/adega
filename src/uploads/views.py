from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from uploads.models import Submission


def upload(request):
    if request.method == 'POST' and request.FILES['historico'] and request.FILES['matricula']:

        submission = Submission.objects.create(author=request.user)
        submission.course = '21A'

        fs = FileSystemStorage(location=submission.path())

        fs.save('historico.xls', request.FILES['historico'])
        fs.save('matricula.xls', request.FILES['matricula'])

        submission.historico.name = submission.path() + '/historico.xls'
        submission.matricula.name = submission.path() + '/matricula.xls'

        submission.save()

        messages.success(request, 'Sua submissão foi realizada com sucesso, por favor aguarde o processamento')

        return redirect('dashboard')

    return render(request, 'uploads/upload.html')
