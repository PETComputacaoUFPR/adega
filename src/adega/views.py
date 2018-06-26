from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as process_logout





@login_required
def dashboard(request):
    degree = request.user.educator.degree.all() 
    return render(request, 'adega/dashboard.html', {'title': 'Dashboard',
        "degrees":degree 
        })


@login_required
def logout(request):
    process_logout(request)

    return redirect('public:index')
