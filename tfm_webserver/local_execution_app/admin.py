# -*- coding: utf-8 -*-

import string
import random
from django.shortcuts import render
from django.conf.urls import url
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
import djqscsv
from .models import User, Exercise


class MyAdminSite(AdminSite):
    '''
        Sobreescribimos la clase Admin por defecto (AdminSite) y la extendemos para que nos permita
        añadir vistas personalizadas.
    '''

admin_site = MyAdminSite()


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ('user_permissions', 'groups', 'exercises')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    list_display = ['username', 'first_name', 'last_name', 'role', 'email', 'last_login', 'date_joined']
    ordering = ['username']

    #Estructura #('group_tittle', {'fields' : ('field1','field2',)}),
    fieldsets = (
        ('User Credentials', {'fields':('username','password',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('JdeRobotKids Info', {'fields':('role','exercises', 'observations',)}),
        ('Permissions', {'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important Dates', {'fields':('last_login','date_joined',)}))

    '''def Code(self, obj):
        return "\n".join([p.code for p in obj.code.all()])'''

    '''def Group(self, obj):
        return "\n".join([p.group for p in obj.code.all()])'''
        
admin.site.register(User, CustomUserAdmin)

# ------------------------------------ EXERCISES ----------------------------------------------

class ExerciseForm( forms.ModelForm ):
    local = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':75}))
    assets = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':75}))
    class Meta:
        model = Exercise
        fields = '__all__' 

class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseForm
    list_display = ['name', 'platform', 'state', 'compute_load', 'observations']

admin.site.register(Exercise, ExerciseAdmin)


