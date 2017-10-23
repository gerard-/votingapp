# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from django.forms.models import BaseInlineFormSet

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

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_change', 'question_people', 'question_category', 'question_advice', 'question_visible', 'question_open']

    def save(self, commit=True):
        q = super(QuestionForm, self).save(commit=commit)
        q.save()
        if not q.choice_set.exists():
            q.choice_set.create(choice_text = 'Overnemen')
            q.choice_set.create(choice_text = 'Niet overnemen')
        return q

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    actions = [copy_question]
    list_display = ['question_text', 'question_visible', 'question_open']
    form = QuestionForm
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(QuestionAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['question_change','question_explanation','question_advice_explanation', 'question_people']:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield
    
class MyUserAdmin(UserAdmin):    
    list_display = ['username', 'is_staff', 'is_superuser']

admin.site.register(Question, QuestionAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
