from django.shortcuts import render, redirect



def dashboard(request):

    return render(request, 'adega/dashboard.html', {'title': 'Dashboard'})


def login(request):

    return render(request, 'adega/login.html', {})
