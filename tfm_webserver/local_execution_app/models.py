# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from time import strftime, localtime
import os
import socket
import base64
import json
import paramiko
import docker
import requests
import shutil
import stat
from datetime import datetime
from local_execution_app.utils import ColorPrint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from github import GithubException
from os.path import isfile, join


class Exercise(models.Model):
    exercise_id = models.CharField(max_length=40, blank=False, unique=True)
    name = models.CharField(max_length=40, blank=False, unique=True)

    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('testing', 'Testing')
    )
    state = models.CharField(max_length=40, blank=False, choices=STATE)

    PLATFORM = (
        ('gazebo', 'Gazebo'),
        ('real', 'Real'),
        ('theory', 'Theory'),
        ('vision', 'Vision'),
        ('tutorials', 'Tutoriales')
    )
    platform = models.CharField(max_length=40, blank=True, choices=PLATFORM)

    LANGUAGE = {
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('scratch', 'Scratch')
    }
    language = models.CharField(max_length=40, choices=LANGUAGE)
    description = models.CharField(max_length=400, blank=False)
    video = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    thumbnail = models.CharField(max_length=100, blank=True)
    assets = models.CharField(max_length=2000, default=json.dumps({"notebook":""})) # JSON Object.
    gui = models.CharField(max_length=2000, blank=True) # Estructura {"client":"", "server":""}
    referee = models.CharField(max_length=2000, blank=True) # Estructura {"client":"", "server":""}
    real = models.CharField(max_length=50, blank=True) # vista para la descarga en real
    local = models.CharField(max_length=2000, blank=True)
    compute_load = models.IntegerField(blank=False, default=100) # Unidades: Unidad de Computo (UC)
    observations = models.TextField(max_length=500, blank=True)
    
    def __unicode__(self):  # __unicode__ for Python 2
        return self.name

    def get_observations(self):
        if self.local:
            return json.loads(self.local)
        else:
            return None
            
    def exercise_location(self,local=False):
        """ Ruta a la carpeta que contiene los archivos propios de cada ejercicio """
        if local:
            return settings.EXERCISES_DIR + '/' + self.language + "/" + self.exercise_id + '/local/'
        else:
            return settings.EXERCISES_DIR + '/' + self.language + "/" + self.exercise_id + '/'

    def exercise_file_location(self,local=False):
        """ Ruta al archivo con el código base (cuadernillo por defecto) del ejercicio """
        assets = json.loads(self.assets)
        if local:
            return settings.BASE_DIR + "/exercises/" + self.language + "/" + self.exercise_id + "/local/" + 'local_' + assets["notebook"]
        else:
            return settings.BASE_DIR + "/exercises/" + self.language + "/" + self.exercise_id + "/" + assets["notebook"]


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('Betatester', 'Betatester'),
        ('profesor', 'Profesor'),
        ('alumno', 'Alumno')
    )

    role = models.CharField(max_length=40, choices=ROLES, blank=True)
    exercises = models.ManyToManyField(Exercise, blank=True)
    #packs = models.ManyToManyField(Pack, blank=True)
    #code = models.ManyToManyField(Code, blank=True)
    observations = models.TextField(max_length=500, blank=True)
    jupyter_port = models.CharField(max_length=10, blank=True)

    # ======================================= RUTAS A ARCHIVOS ===========================================

    def __unicode__(self):  # __unicode__ for Python 2
        return self.username

    def local_user_location(self):
        """ Obtiene el path de la carpeta del usuario en el servidor principal. En ella se almacenan de forma temporal los ejercicios de dicho usuario
        
        Returns:
            str: Path al directorio del usuario
        """
        return settings.USERS_LOCAL_DIR + '/' + self.username + '/'

    def local_user_exercise_location(self, exercise, local=False):
        """ Obtiene el path de la carpeta del ejercicio del usuario en el servidor principal.
        
        Returns:
            str: Path al directorio del ejercicio del usuario
        """
        if local:
            return str(self.local_user_location() + exercise.exercise_id + '/local/')
        else:
            return str(self.local_user_location() + exercise.exercise_id + '/')

    def repo_user_exercise_location(self, exercise, local=False):
        """ Path de la carpeta del ejercicio del usuario en el repositorio de GitHub
        
        Args:
            exercise (Exercise Object): Ejercicio del que obtener la ruta
        
        Returns:
            str: Path del ejercicio del usuario en Github
        """
        if local:
            return  settings.GITHUB_USERS_DIR + self.username + '/' + exercise.exercise_id + '/local'
        else:
            return  settings.GITHUB_USERS_DIR + self.username + '/' + exercise.exercise_id 

    def exercises_files(self, exercise):
        """ Listado de los archivos de la carpeta self.local_user_exercise_location(exercise)"
        
        Args:
            exercise (Exercise Object):  Ejercicio del que obtener los archivos
        
        Returns:
            array : Array con los archivos de la carpeta user.local_user_exercise_location
        """

        local_user_exercise_location = self.local_user_exercise_location(exercise)
        exercises_files = [f for f in os.listdir(local_user_exercise_location) if isfile(join(local_user_exercise_location, f))]

        return exercises_files

    def prepare_directory(self, exercise, local=False):
        """ Prepara los directorios del usuario en el servidor principal. Si no existe, los crea y si existe elimina los existente para
            prepararlos para nuevos archivos. Tipicamente utilizada cuando se van a traer el servidor principal los archivos desde una máquina 
            de la granja para ser subidos a GitHub
        
        Args:
             exercise (Exercise Object):  Ejercicio del que preparar los directorios
        """
        if local:
            if not os.path.isdir(self.local_user_location()):
                os.mkdir(self.local_user_location())
            if os.path.isdir(self.local_user_exercise_location(exercise,local=True)):
                shutil.rmtree(self.local_user_exercise_location(exercise,local=True))
            if os.path.isdir(self.local_user_exercise_location(exercise)):
                shutil.rmtree(self.local_user_exercise_location(exercise))
            os.mkdir(self.local_user_exercise_location(exercise))
            os.mkdir(self.local_user_exercise_location(exercise,local=True))
        else:
            if not os.path.isdir(self.local_user_location()):
                os.mkdir(self.local_user_location())
            if os.path.isdir(self.local_user_exercise_location(exercise)):
                shutil.rmtree(self.local_user_exercise_location(exercise))
            os.mkdir(self.local_user_exercise_location(exercise))


    def gh_push_file(self, content, exercise, file_name,local=False):
        """ Sube a GitHub el contenido de un archivo
        
        Args:
            content (): Contenido del archivo a subir
            exercise (Exercises Object): Ejercicio al que pertenece el archivo
            file_name (str): Nombre del archivo a subir a GitHub
        """
        if local:
            repo_file_path = self.repo_user_exercise_location(exercise, local=True) + "/" + 'local_' + file_name
            if repo_file_path[0] == "/":
                repo_file_path = repo_file_path[1:]
            try:
                file_repo = settings.REPOSITORY.get_contents(repo_file_path)
                commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
                update_message = settings.REPOSITORY.update_file(repo_file_path, commit, content, file_repo.sha)
                print(update_message)
                print("\033[94m Archivo " + repo_file_path + " actualizado en GitHub" + "\033[0m")

            except GithubException as e:
                print(e)
                if e.status == 404:
                    print("\033[93m No existen archivos de la practica " + exercise.exercise_id + " del usuario " + self.username + " en el directorio " + self.repo_user_exercise_location(exercise,local=True) + ". Copiando archivos por defecto." + "\033[0m")
                    commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
                    update_message = settings.REPOSITORY.create_file(repo_file_path, commit, content)
                    print(update_message)
                    print("\033[94m Archivo " + repo_file_path + " subido a GitHub" + "\033[0m")

        else:
            repo_file_path = self.repo_user_exercise_location(exercise) + "/" + file_name
            if repo_file_path[0] == "/":
                repo_file_path = repo_file_path[1:]
            try:
                file_repo = settings.REPOSITORY.get_contents(repo_file_path)
                commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
                update_message = settings.REPOSITORY.update_file(repo_file_path, commit, content, file_repo.sha)
                print(update_message)
                print("\033[94m Archivo " + repo_file_path + " actualizado en GitHub" + "\033[0m")

            except GithubException as e:
                print(e)
                if e.status == 404:
                    print("\033[93m No existen archivos de la practica " + exercise.exercise_id + " del usuario " + self.username + " en el directorio " + self.repo_user_exercise_location(exercise) + ". Copiando archivos por defecto." + "\033[0m")
                    commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
                    update_message = settings.REPOSITORY.create_file(repo_file_path, commit, content)
                    print(update_message)
                    print("\033[94m Archivo " + repo_file_path + " subido a GitHub" + "\033[0m")
        

    def gh_pull_file(self, exercise, file_name):
        """ Obtiene el contenido del archivo con el nombre "file_name" perteneciente al ejercicio correspondiente. Tipicamente utilizado para descargar desde GitHub
        el código del usuario al iniciar una simulación. Puesto que unicamente necesitamos el contenido no lo guardamos en ningún archivo del servidor principal.
        
        Args:
            exercise (Exercises Object): Ejercicio al que pertenece el archivo
            file_name (str): Nombre del archivo
        
        Returns:
            []: Contenido del archivo
        """
        file_contents = settings.REPOSITORY.get_contents(self.repo_user_exercise_location(exercise) + '/' + file_name)
        file_data = base64.b64decode(file_contents.content)

        return file_data


    def gh_pull_exercise(self, exercise, local=False):
        """ Descarga desde GitHub todos los archivos del ejercicio correspodiente.Estos son almacenados en la carpeta self.local_user_exercise_location(exercise)
        del servidor principal
        
        Args:
            exercise (Exercises object): Ejercicio de los archvios a descargar desde GitHub
        """
        if local:
            try:
                repository_directory_content = settings.REPOSITORY.get_contents(self.repo_user_exercise_location(exercise,local=True))
                for file in repository_directory_content:
                    if file.type == "file":
                        file_data = base64.b64decode(file.content)
                        file_out = open(
                            str(self.local_user_exercise_location(exercise,local=True) + file.name), "w")
                        os.chmod(self.local_user_exercise_location(exercise,local=True) + file.name, 0o664)
                        file_out.write(file_data)
                        file_out.close()

            except GithubException as e:
                print(e)
                if e.status == 404:
                    print("\033[93m No existen archivos de la practica " + exercise.exercise_id + '/local/' + " del usuario " + self.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                    assets = json.loads(exercise.assets)
                    print exercise.exercise_file_location(local=True)
                    shutil.copyfile(exercise.exercise_file_location(local=True), self.local_user_exercise_location(exercise,local=True) + 'local_' + assets["notebook"])
        else:
            try:
                repository_directory_content = settings.REPOSITORY.get_contents(self.repo_user_exercise_location(exercise))
                for file in repository_directory_content:
                    if file.type == "file":
                        file_data = base64.b64decode(file.content)
                        file_out = open(
                            str(self.local_user_exercise_location(exercise) + file.name), "w")
                        os.chmod(self.local_user_exercise_location(exercise) + file.name, 0o664)
                        file_out.write(file_data)
                        file_out.close()

            except GithubException as e:
                print(e)
                if e.status == 404:
                    print("\033[93m No existen archivos de la practica " + exercise.exercise_id + " del usuario " + self.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                    assets = json.loads(exercise.assets)
                    shutil.copyfile(exercise.exercise_file_location(), self.local_user_exercise_location(exercise) + assets["notebook"])
