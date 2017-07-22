# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Question, Answer

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(question_visible=True)

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "U dient een keuze te maken",
        })
    if not question.question_open:
        return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "De stemming is gesloten",
                })        
    
    selected_choice.votes += 1
    selected_choice.save()
    
    # Remove previous answer
    Answer.objects.filter(user=request.user, question=question).delete()
    
    # Add the answer
    a = Answer(user=request.user, question=question, choice=selected_choice)
    a.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
