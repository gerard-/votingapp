# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .models import Question, Choice, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice

def copy_question(modeladmin, request, queryset):
    for orig in queryset:
        q = Question(question_text="Kopie van "+orig.question_text)
        q.save()
        for orig_choice in orig.choice_set.all():
            c = Choice(question=q, choice_text=orig_choice.choice_text)
            c.save()

copy_question.short_description = "Kopieer stemmingen"

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    actions = [copy_question]
    list_display = ['question_text', 'question_visible', 'question_open']
    
class MyUserAdmin(UserAdmin):    
    list_display = ['username', 'is_staff', 'is_superuser']

admin.site.register(Question, QuestionAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
