#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# This flask program uncompress and move files from "uploads" folder to
# "running" folder and then, execute the code.
# ------------------------------- Fran Pérez & Ignacio Arranz - 2018 ---

import os
import subprocess
import sys
import signal
import time

sys.path.insert(0, '/home/pi/infraestructura/piBot/descargaLocal/running')

from flask import Flask, request, redirect, url_for, send_from_directory
from flask import flash, render_template, session, abort
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename



### Static variables
UPLOAD_FOLDER = '/home/pi/infraestructura/piBot/descargaLocal/uploads'
CONTEXT = '/home/pi/infraestructura/piBot/descargaLocal'

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'gif', 'zip'])

app = Flask(__name__)
app.config['SECRET_KEY'] = b'hola'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, 
            resources={r"/run": {"origins": "http://0.0.0.0:8001"},\
                       r"/": {"or/home/pi/infraestructura/piBot/descargaLocal/flask-venv/binigins": "http://0.0.0.0:8001"}, \
                       r"/stop": {"origins": "http://0.0.0.0:8001"}, \
                       r"/uploads": {"origins": "http://0.0.0.0:8001"}})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

exercise = None

### Views
# ----------------------------------------------------------------------
#                              INDEX
# ----------------------------------------------------------------------
@app.route("/")
@cross_origin(origin='0.0.0.0:8001', 
                headers=['Content-Type','Authorization'])
def index():
    return render_template('index.html', success=True)
      
        
# ----------------------------------------------------------------------
#                              PARAR
# ----------------------------------------------------------------------
@app.route('/stop', methods=['GET'])
@cross_origin(origin='0.0.0.0:8001', 
                headers=['Content-Type','Authorization'])
def parar():
    global exercise
    
    try:
        #os.kill(exercise.pid, signal.SIGKILL)
        #print('\t',os.getpgid(exercise.pid))
        #print('\t', exercise.pid)
        
        exercise.terminate()
        exercise.wait()
        
        
        #stop = subprocess.Popen([CONTEXT + "/flask-venv/bin/python", CONTEXT + "/running/pibot_obfuscate/stop.py"],
        #                                env={"PYTHONPATH": CONTEXT + "/running/",
        #                                     "JDEROBOT_CONFIG_PATHS": CONTEXT + "/running/pibot_obfuscate"})
        stop = subprocess.Popen([CONTEXT + "/flask-venv/bin/python", CONTEXT + "/stop.py"],
                                        env={"PYTHONPATH": CONTEXT,
                                             "JDEROBOT_CONFIG_PATHS": CONTEXT})
        time.sleep(5)
        stop.kill()
        stop.wait()
        
        '''
        time.sleep(3)
        stop.terminate()
        stop.wait()
        '''
        
        print("deteniendo...")
    except Exception as e:
        print(str(e))
        print("No se ha podido detener el proceso")
    
    return render_template('index.html', success=True)
    

# ----------------------------------------------------------------------
#                             EJECUTAR
# ----------------------------------------------------------------------
@app.route('/run', methods=['GET'])
@cross_origin(origin='0.0.0.0:8001', 
                headers=['Content-Type','Authorization'])
def ejecutar_ejercicio():
    global exercise

    content = subprocess.getoutput('ls ' + CONTEXT + '/uploads/')
    try:
        content = content.split(".")
    except:
        content = content.split()

    print("\n\n")
    print(content)
    
    # If the files are compressed
    if content[-1] == "zip":
        print("\nDecompress zip:\n")
        os.system("unzip -o " + CONTEXT + "/uploads/*.zip -d " + CONTEXT + "/running/")
        print("\nDeleting temporaly files . . .\n")
        os.system("rm " + CONTEXT + "/uploads/*.zip")
        
        # CODE TO RUN THE ROBOT PROGRAM - HERE            
        exercise = subprocess.Popen([CONTEXT + "/flask-venv/bin/python", CONTEXT + "/running/pibot_obfuscate/ejercicio.py"],
                                        env={"PYTHONPATH": CONTEXT + "/running/",
                                             "JDEROBOT_CONFIG_PATHS": CONTEXT + "/running/pibot_obfuscate"})
        #exercise.communicate()

    elif content[-1] == "tar":
        print("Decompressing tar:\n")
        os.system("tar -zxvf " + CONTEXT + "/uploads/exercise.tar -C " + CONTEXT + "/running/")

        # CODE TO RUN THE ROBOT PROGRAM - HERE
        
    else:
        print("Moving files")
        os.system("mv " + CONTEXT + "/uploads/* " + CONTEXT + "/running/")
        # CODE TO RUN THE ROBOT PROGRAM - HERE
    
    response = "Ejecutando ..."
    return(response)


# ----------------------------------------------------------------------
#                   UPLOAD FILES FROM DOCUMENTATION
# ----------------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_program', methods=['GET', 'POST'])
#@cross_origin(origin='0.0.0.0:8001', 
#                headers=['Content-Type','Authorization'])
def upload_program():

    print("\n\n\n")
    print(request.method) 
    os.system("rm "+ UPLOAD_FOLDER + "/*")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("\n\nALLOWED FILE\n\n")
            filename = secure_filename(file.filename)
            print("\n\n\n File Uploaded: " + str(filename) + "\n\n\n")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 
                                    filename))
            #return redirect(url_for('./uploads/' + filename,
            #                        filename=filename))
            print('file uploaded successfully')
            
            print(ejecutar_ejercicio())
            
            # return del POST
            return render_template('index.html', success=True, 
                                    running=True)
    # return del GET
    return render_template('index.html', success=True)
    

# ----------------------------------------------------------------------
#                        MAIN PROGRAM
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
    #app.run(host='0.0.0.0', ssl_context=("./assets/cert.pem", 
                                         #"./assets/key.pem"), 
                                         #   port=8001, 
                                         #   debug=True)
