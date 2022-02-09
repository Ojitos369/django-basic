# Python

# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# User
from .models import *


def index(request):
    latest_question_list = Question.objects.all()
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    return HttpResponse(f"Estas viendo los resultados de la pregunta {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Estas votando a la pregunta {question_id}")