# Python
import datetime as dt
# Django
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.utils import timezone

# User
from .models import *

''' 
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
    question = get_object_or_404(Question, pk = question_id)
    context = {
        'question': question
    }
    return render(request, 'polls/results.html', context)

 '''

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]
        #questions = Question.objects.filter(pub_date__lte = timezone.now())
        #questions = questions.filter(pub_date__gt = timezone.now() - dt.timedelta(days = 1))
        #questions = questions.order_by('-pub_date')[:5]
        #return questions


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question': question,
            'error_message': "No seleccionaste ninguna opción"
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
