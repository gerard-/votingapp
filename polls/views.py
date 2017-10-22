# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.contrib.auth.models import User
from .models import Question, Answer, Choice

def sort_by_number(x):
    s = ''.join(i for i in x.question_text.split('.')[0] if i.isdigit())
    return int(s) if s else 999999

@login_required
def index(request):
    open_questions = Question.objects.filter(question_visible=True, question_open=True)
    open_not_voted_questions = sorted(open_questions.exclude(answer__user=request.user), key=sort_by_number)
    open_voted_questions = sorted(open_questions.filter(answer__user=request.user), key=sort_by_number)
    closed_questions = sorted(Question.objects.filter(question_visible=True, question_open=False), key=sort_by_number)
    if request.user.is_staff:
        hidden_questions = sorted(Question.objects.filter(question_visible=False), key=sort_by_number)
    else:
        hidden_questions = []
    return render(request, 'polls/index.html', {
                    'open_not_voted_questions': open_not_voted_questions,
                    'open_voted_questions': open_voted_questions,
                    'closed_questions': closed_questions,
                    'hidden_questions': hidden_questions,
                })

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(question_visible=True)
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        for question in context['question_list']:
            question.user_voted = Answer.objects.filter(user=self.request.user,question=question).exists()
        return context        

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['user_voted'] = Answer.objects.filter(user=self.request.user,question=context['question']).exists()
        return context

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['user_voted'] = Answer.objects.filter(user=self.request.user,question=context['question']).exists()
        return context

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
    if request.user.is_staff:
        return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "Organisatoren mogen niet stemmen",
                })
    
    # Remove previous answer
    Answer.objects.filter(user=request.user, question=question).delete()
    
    # Add the answer
    a = Answer(user=request.user, question=question, choice=selected_choice)
    a.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@login_required
def cancel_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.question_open:
        return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "De stemming is gesloten",
                })
    # Remove previous answer
    Answer.objects.filter(user=request.user, question=question).delete()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def usergen(request):
    if not request.user.is_superuser:
        return render(request, 'polls/usergen.html', {
                    'error_message': "U bent geen admin",
                })
    return render(request, 'polls/usergen.html')
    
@login_required
def open(request, question_id):
    if not request.user.is_superuser:
        return render(request, 'polls/results.html', {
                    'error_message': "U bent geen admin",
                })
    question = get_object_or_404(Question, pk=question_id)
    question.question_open = True
    question.question_visible = True
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@login_required
def close(request, question_id):
    if not request.user.is_superuser:
        return render(request, 'polls/results.html', {
                    'error_message': "U bent geen admin",
                })
    question = get_object_or_404(Question, pk=question_id)
    question.question_open = False
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@login_required
def show(request, question_id):
    if not request.user.is_superuser:
        return render(request, 'polls/results.html', {
                    'error_message': "U bent geen admin",
                })
    question = get_object_or_404(Question, pk=question_id)
    question.question_visible = True
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
@login_required
def hide(request, question_id):
    if not request.user.is_superuser:
        return render(request, 'polls/results.html', {
                    'error_message': "U bent geen admin",
                })
    question = get_object_or_404(Question, pk=question_id)
    question.question_visible = False
    question.question_open = False
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def reset(request, question_id):
    if not request.user.is_superuser:
        return render(request, 'polls/results.html', {
                    'error_message': "U bent geen admin",
                })
    question = get_object_or_404(Question, pk=question_id)
    Answer.objects.filter(question=question).delete()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def usergen_generate(request):
    if not request.user.is_superuser:
        return render(request, 'polls/usergen.html', {
                    'error_message': "U bent geen admin",
                })
    # See what the highest "voter id" is
    highest = 0
    for user in User.objects.all():
        try:
            value = int(user.username)
            if value > highest:
                highest = value
        except (ValueError):
            pass
            
    count=int(request.POST['count'])
    result = []
    for i in range(highest+1, highest+1+count):
        username=str(i)
        password = User.objects.make_random_password(length=12, allowed_chars="0123456789")
        u = User.objects.create_user(username=username, password=password)
        password = re.sub(r"([0-9][0-9][0-9])", r"\1 ", password)
        result.append({"username":username,"password":password})
    
    return render(request, 'polls/usergen_result.html', {
                'users': result
            })
