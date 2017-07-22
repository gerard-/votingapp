# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField("Tekst", max_length=200)
    question_visible = models.BooleanField("Zichtbaar", default=False)
    question_open = models.BooleanField("Open", default=False)
    
    def __str__(self):
        return self.question_text
        
    class Meta:
        verbose_name = 'Stemming'
        verbose_name_plural = 'Stemmingen'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Tekst",max_length=200)

    def __str__(self):
        return self.choice_text
        
    class Meta:
        verbose_name = 'Keuze'
        verbose_name_plural = 'Keuzes'        

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    class Meta:
        # Allow a user to only answer a question once
        unique_together = ('user', 'question',)

    def __str__(self):
        return str(self.user)+": "+str(self.question)+"->"+str(self.choice)
