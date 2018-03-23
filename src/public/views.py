from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from public.forms import LoginForm


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)

                return redirect(request.GET.get('next', 'dashboard'))
            else:
                return redirect('public:index')

    return render(request, 'public/index.html', {'form': LoginForm()})

