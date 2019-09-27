from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question 
from django.utils import timezone
from .forms import QuestionForm

# Create your views here.

@login_required
def question_list(request):
    questions = Question.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'faq/question_list.html', {"title" : "FAQ",
                                                     "hide_navbar" : True,
                                                     'questions' : questions
                                                    })

def question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('faq:question_list')
    else:
        form = QuestionForm()
        return render(request, 'faq/question_new.html', {"title" : "FAQ",
                                                        "hide_navbar" : True,
                                                        'form': form
                                                        })