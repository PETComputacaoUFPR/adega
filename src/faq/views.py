from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def question_list(request):
    
    return render(request, 'faq/question_list.html', {"title": "FAQ",
                                                     "hide_navbar": True
                                                    })