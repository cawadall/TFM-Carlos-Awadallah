# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Exercise
import os
import io
import time
from time import strftime, localtime
import socket
import subprocess
import shutil
import json
from collections import OrderedDict
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, FileResponse
from django.utils.encoding import force_bytes, force_text
from os.path import isfile, join
import docker
from django.contrib.admin.views.decorators import staff_member_required
import paramiko
import requests
from datetime import datetime
import re
from django.db.models import F, Q
from django.utils.translation import ugettext_lazy as _
from utils import ColorPrint, ipynb_to_python, copy_import, build_zip
from requests.exceptions import ConnectionError

# PyGithub for Github Repositorys
from github import Github, GithubException
import base64

User = get_user_model() # Extended User Model

# ==============================================================================
# ================================== INDEX =====================================
# ==============================================================================

USER = 'admin'
AUTENTICATED = True

def index(request):
    """ Index of the Application """
    
    context = {
        "authenticate": False
    }
    return render(request, 'local_execution_app/index.html', context)


# ==============================================================================
# ============================== MAIN PAGE =====================================
# ==============================================================================

def main_page(request):
    """ Main Page - Set of Exercises """
   
    if AUTENTICATED:
        user = User.objects.get(username='admin')#request.user.username
        context = {
            "authenticate": True,
            "user": user
        }
        response = render(request, 'local_execution_app/main_page.html', context)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    else:
        context = {
            "authenticate": False
        }
        return render(request, 'local_execution_app/login.html', context)


def exit_local(request):
    """ Exit Local Execution - Saving of progress and garbage collector """

    user = User.objects.get(username='admin')

    if request.method == 'POST':

        ### Exitting exercise ###
        exercise = Exercise.objects.get(exercise_id=request.POST['exercise_id'])
        # Obtain Notebook and session id
        filled_notebook = request.POST['filledNotebook'] 
        kernel_session = request.POST['kernelSession']
        files_to_delete = request.POST['files2delete']

        assets = json.loads(exercise.assets)
        if filled_notebook != "undefined":

            if "Competitive" in exercise.get_observations():
                # do not save competitive exercises!
                pass
            else:
                if exercise.platform == "gazebo":
                    user.gh_push_file(filled_notebook, exercise, assets["notebook"],local=True)
                else:
                    user.gh_push_file(filled_notebook, exercise, assets["notebook"])

        jupyter_server_ip = '127.0.0.1'

        if request.LANGUAGE_CODE == 'es':
            msg = "Simulación finalizada con éxito! No olvides parar el contenedor !"
        else:
            msg = "Simulation successfully completed! Don't forget to stop the container!"
            
        context = {
            "authenticate": True,
            "success": True,
            "user": user,
            "message": msg,
            "exit_mixed_execution": True,
            "port": user.jupyter_port,
            "ip_address": jupyter_server_ip,
            "file_names": files_to_delete,
            #"token": user.jupyter_token,
            "session": kernel_session,
            "exit_mixed_execution": True,
        }

    else:

        context = {
            "authenticate": True,
            "user": user
        }

    return render(request, 'local_execution_app/main_page.html', context)


# ==============================================================================
# ====================== MIXED EXECUTION SIMULATION ============================
# ==============================================================================

def local(request):
    """ Local Simulation Page (Mixed Execution) """

    jupyter_server_ip = '127.0.0.1' # Local Execution (localhost)
    # Extract port and token from the form
    jupyter_server_port = request.POST['port']
    #_token = request.POST['token']
    nbcontent = ""
    codefile = ""
    configfile = ""
    assets=[]

    exercise = Exercise.objects.get(exercise_id=request.POST['exercise'])
    # Update user information with the token and teh port
    user = User.objects.get(username='admin')
    user.jupyter_port = jupyter_server_port
    #user.jupyter_token = _token
    user.save()
    if exercise.platform != "gazebo":
        # ----------------------------------------------- PATHS ------------------------------------------------------------
        exercise_location = exercise.exercise_location()
        user_exercise_location = user.local_user_exercise_location(exercise)
        images_exercise_location = os.path.join(exercise_location, 'img')
        # ------------------------------------------ PREPARE DIRECTORY -----------------------------------------------------
        user.prepare_directory(exercise)
        # ----------------------------------------- DOWNLOAD USER FILES ----------------------------------------------------
        user.gh_pull_exercise(exercise)

    else:
        # ----------------------------------------------- PATHS ------------------------------------------------------------
        exercise_location = exercise.exercise_location()
        images_exercise_location = os.path.join(exercise_location, 'img')
        exercise_location = exercise.exercise_location(local=True)
        user_exercise_location = user.local_user_exercise_location(exercise,local=True)
        # ------------------------------------------ PREPARE DIRECTORY -----------------------------------------------------
        user.prepare_directory(exercise,local=True)
        # ----------------------------------------- DOWNLOAD USER FILES ----------------------------------------------------
        user.gh_pull_exercise(exercise,local=True)

    try:       
        for filename in os.listdir(user_exercise_location):
            with io.open(os.path.join(user_exercise_location, filename), 'r', encoding='utf8') as f:                    
                if filename.endswith(".ipynb"):
                    nbcontent = [filename, f.read()]
                    nbname = filename
                    nbcontent = json.dumps(nbcontent, indent = 2, encoding="utf8")

        for filename in [f for f in os.listdir(exercise_location)  if isfile(join(exercise_location, f))]:
            with io.open(os.path.join(exercise_location, filename), 'r', encoding='utf8') as f:                    
                if filename.endswith(".py"):
                    rawcode = f.read()
                    codefile = [filename, json.dumps(rawcode, indent = 2, encoding="utf8")]
                    # Convert file to json object
                    codefile = json.dumps(codefile, indent = 2, encoding="utf8")
                elif filename.endswith(".yml"):
                    rawconfig = f.read()
                    configfile = [filename, json.dumps(rawconfig, indent = 2, encoding="utf8")]
                    # Convert file to json object
                    configfile = json.dumps(configfile, indent = 2, encoding="utf8")
        for filename in [f for f in os.listdir(images_exercise_location)  if isfile(join(images_exercise_location, f))]:
            with io.open(os.path.join(images_exercise_location, filename), 'r', encoding='utf8') as f:             
                if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".mat") or filename.endswith(".TIF"):
                    f.close()
                    # Send images codified in base64
                    with io.open(os.path.join(images_exercise_location, filename), 'rb') as f:
                        img = f.read()
                        image_data = [filename, base64.b64encode(img)]
                        assets.append(image_data)

        if assets:
            try:
                # convert auxiliary resources of the exercise to JSON object
                assets = json.dumps(assets, indent=2)
            except Exception, e:
                print e

        # Drivers
        driver = None
        if "drivers" in json.loads(exercise.assets):
            driver = json.loads(exercise.assets)["drivers"]

        # Gazebo
        gzweb_url = None
        if exercise.platform == "gazebo":
            gzweb_url = 'http://127.0.0.1:8080'

        context = {
            'exercise': exercise,
            "port": user.jupyter_port,
            "ip_address": jupyter_server_ip,
            #"token": user.jupyter_token,
            "notebook": nbcontent,
            "nbname": nbname,
            "codefile": codefile,
            "configfile": configfile,
            "assets": assets,
            "driver": driver,
            "simulation_site": True,
            "authenticate": True,
            "simulation_type" : "local",
            "gzweb_url": gzweb_url,
        }

        if exercise.gui:
            exercise.gui = json.loads(exercise.gui)
            gui_port = '9002'
            context["gui_url"] = "ws://" + '127.0.0.1' + ":" + gui_port 
            if exercise.gui["client"]: context["gui"] = exercise.gui["client"]

        if exercise.referee:
            exercise.referee = json.loads(exercise.referee)
            referee_port = '9001'
            context["referee_url"] = "ws://" + '127.0.0.1' + ":" + referee_port
            if exercise.referee["client"]: context["referee"] = exercise.referee["client"]

        if "viewer" in json.loads(exercise.assets):
            algorithm_port = '9001'
            context["gui_url"] = "ws://" + '127.0.0.1' + ":" + algorithm_port 
            camera_port = '9002'
            context["cam_url"] = "ws://" + '127.0.0.1' + ":" + camera_port 

        context["language"] = request.LANGUAGE_CODE

    except Exception, e:
        print e
        if request.LANGUAGE_CODE == 'es':
            msg = "Lo sentimos, algo salió mal"
        else:
            msg = "Oops! Something went wrong"
        
        context = {
            "authenticate": True,
            "message":  msg,
            "error": True,
        }
    response = render(request, 'local_execution_app/local.html', context)
    response["Access-Control-Allow-Origin"] = "*"
    return response


def validate_username(request):
    from django.http import JsonResponse
    """ View that allows to check if certain user exists in the DDBB """
    username = request.GET.get('username', None)

    exercise = Exercise.objects.get(exercise_id=request.GET.get('exercise_id', None))
    nbcontent = None
    if User.objects.filter(username__iexact=username).exists():

        user = User.objects.get(username=username)

        # ----------------------------------------------- PATH ----------------------------------------------------------------
        exercise_location = exercise.exercise_location(local=True)
        user_exercise_location = user.local_user_exercise_location(exercise,local=True)
        # ----------------------------------------- PREPARE DIRECTORY ---------------------------------------------------------
        user.prepare_directory(exercise,local=True)
        # ---------------------------------------- DOWNLOAD USER FILES --------------------------------------------------------
        user.gh_pull_exercise(exercise,local=True)

        try:       
            for filename in os.listdir(user_exercise_location):
                with io.open(os.path.join(user_exercise_location, filename), 'r', encoding='utf8') as f:                    
                    if filename.endswith(".ipynb"):
                        nbcontent = [filename, f.read()]
                        nbname = filename
                        nbcontent = json.dumps(nbcontent, indent = 2, encoding="utf8")
        except(e):
            print e

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
        'notebook': nbcontent
    }
    return JsonResponse(data)

def local_competitive_exercise(request):
    """ Competitive Local Simulatión Page """

    jupyter_server_ip = '127.0.0.1'
    jupyter_server_port = request.POST['port']
    codefile = ""
    configfile = ""
    assets=[]

    exercise = Exercise.objects.get(exercise_id=request.POST['exercise'])
    user = User.objects.get(username='admin')
    user.jupyter_port = jupyter_server_port
    #user.jupyter_token = _token
    user.save()

    exercise_location = exercise.exercise_location()
    images_exercise_location = os.path.join(exercise_location, 'img')
    exercise_location = exercise.exercise_location(local=True)
    user_exercise_location = user.local_user_exercise_location(exercise,local=True)
    user.prepare_directory(exercise,local=True)
    user.gh_pull_exercise(exercise,local=True)

    try:       
        for filename in [f for f in os.listdir(exercise_location)  if isfile(join(exercise_location, f))]:
            with io.open(os.path.join(exercise_location, filename), 'r', encoding='utf8') as f:                    
                if filename.endswith(".py"):
                    rawcode = f.read()
                    codefile = [filename, json.dumps(rawcode, indent = 2, encoding="utf8")]
                    codefile = json.dumps(codefile, indent = 2, encoding="utf8")
                elif filename.endswith(".yml"):
                    rawconfig = f.read()
                    configfile = [filename, json.dumps(rawconfig, indent = 2, encoding="utf8")]
                    configfile = json.dumps(configfile, indent = 2, encoding="utf8")
        for filename in [f for f in os.listdir(images_exercise_location)  if isfile(join(images_exercise_location, f))]:
            with io.open(os.path.join(images_exercise_location, filename), 'r', encoding='utf8') as f:             
                if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".mat") or filename.endswith(".TIF"):
                    f.close()
                    with io.open(os.path.join(images_exercise_location, filename), 'rb') as f:
                        img = f.read()
                        image_data = [filename, base64.b64encode(img)]
                        assets.append(image_data)

        if assets:
            try:
                assets = json.dumps(assets, indent=2)
            except Exception, e:
                print e

         # Gazebo
        gzweb_url = None
        if exercise.platform == "gazebo" or exercise.platform == "vision":
            gzweb_url = 'http://127.0.0.1:8080'

        coordinator_url = "ws://127.0.0.1:9001"

        context = {
            'exercise': exercise,
            "port": user.jupyter_port,
            "ip_address": jupyter_server_ip,
            "codefile": codefile,
            "configfile": configfile,
            "assets": assets,
            "simulation_site": True,
            "authenticate": True,
            "simulation_type" : "local",
            "gzweb_url": gzweb_url,
            "coordinator_url": coordinator_url,
        }
        context["language"] = request.LANGUAGE_CODE


    except Exception, e:
        print e
        if request.LANGUAGE_CODE == 'es':
            msg = "Lo sentimos, algo salió mal"
        else:
            msg = "Oops! Something went wrong"
        
        context = {
            "authenticate": True,
            "message":  msg,
            "error": True,
        }
    return render(request, 'local_execution_app/local_competitive_exercise.html', context)

def download_exercise(request, exercise_id):
    '''Descarga y prepara los ficheros necesarios para enviar al piBot.'''

    # Peticiones a la base de datos
    user = User.objects.get(username='admin')
    exercise = Exercise.objects.get(exercise_id=exercise_id)
    # Rutas
    user_exercise_location = user.local_user_exercise_location(exercise)
    local_user_exercise_location = ''
    # Variables
    assets = json.loads(exercise.assets)

    # OBTENER EL CODIGO DE UN POST????
    
    filename_ipynb = exercise_id + ".ipynb"
    #host_ip = simulation.host_ip
    filename_py = "ejercicio.py"

    body = json.loads(request.body)
    notebook_content = body["codigo"]

    with io.open(os.path.join(user_exercise_location, filename_ipynb), 'w', encoding='utf8') as f:                    
        f.write(notebook_content)

    if os.path.exists(os.path.join(user_exercise_location, "ejercicio.py")):
        os.remove(os.path.join(user_exercise_location, "ejercicio.py"))
    try:
        ipynb_to_python(user_exercise_location, filename_ipynb, filename_py)
    except Exception as e:
        print(e)
        print(ColorPrint.RED + "AAAAAAAAAAA" + str(e) + ColorPrint.END)

        context = {
            "authenticate": True,
            "message":  "Error en la descarga. Por favor inténtelo de nuevo más tarde.",
            "error": True,
        }
        return render(request, 'local_execution_app/main_page.html', context)

    try:
        
        copy_import("from pibot.pibot import PiBot", settings.DRIVERS_DIR + "/pibot/piBot.py", user_exercise_location + "/" + filename_py)
        path_to_zip, success = build_zip(exercise_id, user, settings.BASE_DIR, local_user_exercise_location, user_exercise_location)
    except Exception as e:
        print(e)
        print(ColorPrint.RED + "Error en cambiar los imports o en construir el ZIP" + str(e) + ColorPrint.END)

        context = {
            "authenticate": True,
            "message":  "Error en la descarga. Por favor inténtelo de nuevo más tarde.",
            "error": True,
        }
        return render(request, 'local_execution_app/main_page.html', context)
    
    if success:
        # Host to build the path to zip
        host = request.get_host()
        protocol = request.scheme

        context = {
            "authenticate": True,
            "message":  "Descarga realizada con éxito!",
        }
        print("\n\n\n" + path_to_zip + "\n\n\n")
        #return redirect(protocol + "://" + host + path_to_zip)
        response = FileResponse(open(path_to_zip, 'rb'), content_type='x-zip-compressed')
        return response
    else:
        context = {
            "authenticate": True,
            "error" : True,
            "message":  "Descarga fallida!",
        }
        return render(request, 'local_execution_app/main_page.html', context)



def error_handler404(request):
    """ 404 Error Page """
    return render(request, 'local_execution_app/error_page/404_error.html', {}, status=404)


def error_handler500(request):
    """ 500 Error Page """
    return render(request, 'local_execution_app/error_page/500_error.html', status=500)


########################## TESTING VIEEEEEW ###################################
def testing(request):
    return redirect('/main_page')
