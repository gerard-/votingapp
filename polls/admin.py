# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Question, Choice, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
