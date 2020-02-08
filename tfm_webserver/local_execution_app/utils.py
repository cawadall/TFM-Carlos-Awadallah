# -*- coding: utf-8 -*-

import os
import shutil
from django.conf import settings
import errno

class ColorPrint():
    """ Clase con las claves de todos los colores disponible para pintar en la consola. 
        USO => ColorPrint.COLOR + str + ColorPrint.END """

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mkdir_p(path):
    """mkdir -p"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def ipynb_to_python(location, filename_in, filename_out):
    """ Converts ipynb to python file"""

    success = False

    try:  
        # Convert IPYNB to PY
        print("\n\njupyter nbconvert --to python " + os.path.join(location, filename_in))

        os.system("jupyter nbconvert --to python " +
                  os.path.join(location, filename_in) + " --output " + filename_out)

        success = True

    except Exception as e:
        print(e)
        print("Error al convertir el cuadernillo: " + str(e))

    return success

def copy_import(text, text_to_replace, file):
    """ Copy in the exercise the contents of the driver to unify 
       everything in a file. """

    os.popen("sed '/^from __future__ import print_function/{s/^/#/}' -i " + file)
    #os.popen("sed -e '\$a\' -i " + text_to_replace)
    os.system("echo '\n\r' >> " + text_to_replace)

    os.popen("sed '/" + text + "/{ \n\t s/" + text +
             "//g \n\t r " + text_to_replace + "\n}' -i " + file)

def build_zip(exercise_id, user, base_dir, local_user_exercise_location, user_exercise_location):
    """ Build a zip to send to the pibot with the driver and the necessary files """

    success = False

    # 1.-Check if the container is running. If not, it is created.
    '''docker_client = docker.from_env()
    try:
        print("\nObteniendo información del contenedor . . .\n")
        container = docker_client.containers.get("obfuscator_container")
    except docker.errors.NotFound:
        print("\nArrancando el contenedor . . .\n")
        run_obfuscator_container(docker_client)'''
    ### 2.- Files manargement. A function prepares the skeleton for ofuscation.
    print("=========== PREPARANDO ENTORNO =========================")
    if os.path.exists(os.path.join(user_exercise_location, "PiBot.zip")):
        os.remove(os.path.join(user_exercise_location, "PiBot.zip"))
    #mkdir_p(os.path.join(user_exercise_location, "pibot_obfuscate"))
    #if os.path.exists(os.path.join(user_exercise_location, "pibot_obfuscate", "ejercicio.py")):
        #os.remove(os.path.join(user_exercise_location, "pibot_obfuscate", "ejercicio.py"))
    #prepare_real_execution(user)
    
    #shutil.move(os.path.join(user_exercise_location, "ejercicio.py"), os.path.join(user_exercise_location, "pibot_obfuscate"))    
    ### 3.- Run the obfuscation
    #os.system('docker exec -i obfuscator_container /bin/bash obfuscator.sh ' + user.username)
    ### 4.- Preparing files to building zip.
    shutil.copy(os.path.join(settings.DRIVERS_DIR, "pibot", "pibot.yml"), os.path.join(user_exercise_location))
    ### 5.- Zip compress.
    os.system("cd " + os.path.join(user_exercise_location) + " && zip -r PiBot.zip * ")
    ### 6 and 7.- Move the zip obfuscated to previous folder - Path to PiBot.zip
    path_to_zip = os.path.join(user_exercise_location, "PiBot.zip")

   
    print("\n---------------------------------")
    print(path_to_zip)
    print("---------------------------------\n")
    success = True
    return path_to_zip, success
