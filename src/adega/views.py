from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required
def index(request):
    try:
        degree = request.user.teacher.degree.all()
        if len(degree) > 0:
            return redirect('degree:index', degree_id=degree[0].code)
    except ObjectDoesNotExist:
        pass

    return render(request, 'adega/no_degree.html')

def developers(request):
#    try:
#        degree = request.user.teacher.degree.all()
#        return render(request, 'adega/developers.html', {'curso': degree[0]})
#    except ObjectDoesNotExist:
#        return render(request, 'adega/developers.html')
#    except AttributeError:
#        return render(request, 'adega/developers.html')
    return render(request, 'adega/developers.html')
