# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    ADVICE = (
        ('positive', 'Overnemen'),
        ('neutral', 'Neutraal'),
        ('negative', 'Niet overnemen'),
    )
        
    question_text = models.CharField("Titel", max_length=2000)
    question_change = models.CharField("Wijziging", max_length=4000, default="")
    question_people = models.CharField("Indieners", max_length=4000, default="")
    question_category = models.IntegerField("Category", default=2, choices=((1,'1'),(2,'2'),(3,'3')))
    question_advice = models.CharField("Advies Programmacommissie", choices=ADVICE, max_length=4000, default="neutral")

    question_visible = models.BooleanField("Zichtbaar", default=False)
    question_open = models.BooleanField("Open", default=False)
    
    def __str__(self):
        return self.question_text
        
    class Meta:
        verbose_name = 'stemming'
        verbose_name_plural = 'stemmingen'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Tekst",max_length=2000)

    def __str__(self):
        return self.choice_text
        
    class Meta:
        verbose_name = 'keuze'
        verbose_name_plural = 'keuzes'        

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    class Meta:
        # Allow a user to only answer a question once
        unique_together = ('user', 'question',)

    def __str__(self):
        return str(self.user)+": "+str(self.question)+"->"+str(self.choice)
