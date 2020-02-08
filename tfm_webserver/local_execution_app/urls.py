# -*- coding: utf-8 -*-

from django.conf.urls import *  
from local_execution_app import views
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
	url(r'^$', views.index), # Cover page
	url(r'^main_page', views.main_page), # Main page. List of exercises
	
	### SIMULACIÓN EJERCICIO ###
	#url(r'^simulation/(?P<simulation_type>[\w\-]+)/(?P<exercise_id>[\w\-]+)', views.simulation_exercise), # Simulation
    url(r'^local', views.local, name='local'), # Local Execution Page
	url(r'^exit_local', views.exit_local, name='exit_local'), # Exit Local Execution Page
	#url(r'^exit_simulation', views.exit_simulation), # Vista de transición al salir de una simulación
    url(r'^download_exercise/(?P<exercise_id>[\w\-]+)', views.download_exercise), # Descarga el proyecto a la raspberry
	
	### TESTING ###
	url(r'^testing', views.testing), # testing view
    url(r'^competitive', views.local_competitive_exercise, name="competitive"), # Local Execution of Competitive exercises 
    url(r'^validate_username', views.validate_username),
]
