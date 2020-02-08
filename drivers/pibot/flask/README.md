# Ejecución en real - RaspberryPi

* [1. Estructura](#1-arbol-ficheros)
* [2. Raspap-WebGui.](#2-raspap-webgui)
    + [2.1. Reinicio Raspap-WebGui](#21-reinicio-raspap)
    + [2.2. Conmutar entre Wifi y hostpotd](#22-conmutar-internet-hostpotd)
    + [2.3. Acceso a internet/red wifi en la raspberry Pi](#23-acceso-internet)
    + [2.4. Reinicio del RaspAp](#24-reinicio-raspap)
    + [2.5. Conectar a internet](#25-conectar-internet)
    + [2.6. Emitir Wifi](#26-emitir-wifi)
* [3. Instalar entorno virtual](#3-instalar-entorno-virtual)
    + [3.1. Librerías necesarias](#31-librerias-necesarias)
    + [3.2. Librerías `pip` necesarias.](#32-librerias-pip-necesarias)
    + [3.3. Debug mode Flask](#33-debug-flask)
    + [3.4. Flask como servicio](#34-flask-como-servicio)
* [4. Demonio para activar `GPIO`](#4-demonio-activar-gpio)
* [5. Inventario](#5-inventanrio)



<a name="1-arbol-ficheros"></a>
## 1. Árbol de ficheros del driver real

```bash
PiBot/
├── __init__.py
├── Kibotics.yml
├── PiBot.py
└── real
    ├── __init__.py
    └── piBot.py
```

<a name="2-raspap-webgui"></a>
## 2. Raspap-webgui
Para que la RaspberryPi pueda emitir wifi para que otros dispositivos se conecten a él se utiliza el programa [raspap-webgui](https://github.com/billz/raspap-webgui).


Para descargar el script de instalación:

```bash
wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap
sudo wget http://www.fars-robotics.net/install-wifi -O /usr/bin/install-wifi`
```

Si está descargado, copiarlo a

```bash
cp install-wifi /usr/bin
```

Una vez descargado/copiado ejecutar:

```
sudo chmod +x /usr/bin/install-wifi
sudo install-wifi
```

[Fuente](http://romcheckfail.com/tl-wn823n-raspberry-pi-3-wireless-fix/)


<a name="21-reinicio-raspap"></a>
### 2.1. Reinicio del RaspAp

Si la pi se ha conectado a otra red wifi desde su chip, para que funcione RaspAp hay que olvidarla.
Para eso hay que borrar las entradas del wpa_supplicant:
```
nano /etc/wpa_supplicant/wpa_supplicant.conf
```
y borrar las entradas de todas las redes wifi a las que se haya conectado, por ejemplo:

```
network={
	ssid="wireless_urjc"
	key_mgmt=NONE
}
```
Reiniciar la pi después para iniciar RaspAp.


<a name="22-conmutar-internet-hostpotd"></a>
### 2.2. Conmutar entre Internet y red Wifi generada por la Pi

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:8001/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 282-807-764
```

<a name="23-acceso-internet"></a>
### 2.3. Acceso a internet/red wifi en la raspberry Pi

Acceso a internet/red wifi en la raspberry Pi. Conmutar entre Internet y red Wifi generada por la Pi.

Archivos involucrados:

```bash
/etc/dhcpcd.conf
```

#### Para que la raspb genere la red wifi
```bash
interface wlan0
static ip_addesss=10.3.141.1/24
static routers=10.3.141.1
static domain_name_servers=1.1.1.1 8.8.8.8
static domain_search=1.1.1.1 8.8.8.8
```

#### Acceso a internet usando un dongle
```bash
interface wlan1
static ip_addesss=
static routers=193.147.79.1
static domain_name_servers=1.1.1.1 8.8.8.8
static domain_search=1.1.1.1 8.8.8.8
```

#### Para acceso a internet vía eth0
```bash
interface eth0
static ip_addesss=193.147.79.190
static routers=193.147.79.1
static domain_name_servers=1.1.1.1 8.8.8.8
static domain_search=1.1.1.1 8.8.8.8
sudo service dhcpcd restart sudo service networking restart
```

Utilizar los scripts alojados en el directorio `scripts`.


<a name="24-reinicio-raspap"></a>
### 2.4. Reinicio del RaspAp

Si la pi se ha conectado a otra red wifi desde su chip, para que funcione RaspAp hay que olvidarla.
Para eso hay que borrar las entradas del wpa_supplicant:

```
nano /etc/wpa_supplicant/wpa_supplicant.conf
```

y borrar las entradas de todas las redes wifi a las que se haya conectado, por ejemplo:

```
network={
	ssid="wireless_urjc"
	key_mgmt=NONE
}
```

Reiniciar la pi después para iniciar RaspAp.


<a name="25-conectar-internet"></a>
### 2.5. Conectar a internet

Ejecutar el script:

```bash
./connect_internet.sh
```

<a name="26-emitir-wifi"></a>
### 2.6. Emitir Wifi

Ejecutar el script:

```bash
./broadcast_wifi.sh
```




a name="3-instalar-entorno-virtual"></a>
## 3. Instalar entorno virtual
Por defecto se está instalando el *virtualenv* en el `home`  por eso la terminal devuelve que no existe el paquete...y hay que ir a mano a:

```bash
/home/"user"/.local/lib/python3.5/site-packages/virtualenv.py <<opciones>>
```

Para crear un entorno virtual con Python 3 sin paquetes heredados en la carpeta oculta en el `/home/.virtualenvs`: 

```bash
virtualenv -p python3 --no-site-packages ~/.virtualenvs/my-env-borrame
```

<a name="31-librerias-necesarias"></a>
### 3.1. Librerías necesarias

Librerías `apt` necesarias:

```
sudo apt install python3-numpy
sudo apt install libatlas-base-dev
sudo apt install libjasper-dev 
sudo apt install libqtgui4
sudo apt install python3-pyqt5
sudo apt install libqt4-test
```

<a name="32-librerias-pip-necesarias"></a>
#### 3.2. Librerías `pip` necesarias.

La lista de librerías necesarias para el funcionamiento es la siguiente (*Nota: para instalar todas utilizar la sentencia que se muestra después*):

```bash
asn1crypto==0.24.0
cffi==1.11.5
Click==7.0
cryptography==2.4.2## Acceso a internet/red wifi en la raspberry Pi
```

#### Dependencias

```bash
Flask==1.0.2
Flask-Cache==0.13.1
Flask-Cors==3.0.7
idna==2.7
imutils==0.5.2
itsdangerous==1.1.0
jderobot-config==0.1.1
jderobot-interfaces-python==0.1.5
Jinja2==2.10
MarkupSafe==1.1.0
numpy==1.16.0
opencv-python==3.4.4.19
picamera==1.13
pigpio==1.42
pycparser==2.19
pyOpenSSL==18.0.0
PyYAML==3.13
RPi.GPIO==0.6.5
six==1.11.0
Werkzeug==0.14.1
```

Instalar todas usando el [archivo del repositorio](https://github.com/jderobot-hub/kibotics-drivers/blob/master/piBot/flask/requirements.txt):

```bash
pip install -r requirements.txt
```


<a name="33-debug-flask"></a>
#### 3.3. Debug mode Flask

Lanzar flask:

```bash
export FLASK_ENV=development
flask run
```

Otra vía sería, con el entorno virtual activado, en la carpeta `flask`:
```bash
python kibotics.py
```

<a name="34-flask-como-servicio"></a>
### 3.4. Flask como servicio

El servidor `flask` que se utiliza es lanzado como servicio. El archivo de configuración puede encontrarse en la carpeta `assets` del repositorio. El contenido es el siguiente:

```service
[Unit]
Description=FlaskRUN
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/infraestructura/piBot/descarga_local/
Type=idle
ExecStart=/usr/bin/python3 /home/pi/infraestructura/piBot/descarga_local/kibotics.py

[Install]
WantedBy=multi-user.target
```

Este fichero, llamado `kibotics.service` se encuentra alojado en el siguiente directorio (`/lib` y/o `/etc/`):

```bash
/etc/systemd/system/kibotics.service
```

Reiniciar el servicio de *demonios*:

```bash
sudo systemctl daemon-reload
sudo systemctl enable kibotics.service
```

Para la gestión del servicio:

```bash
sudo service start|stop|status kibotics
```

<a name="4-demonio-activar-gpio"></a>
## 4. Demonio para activar `GPIO`

Añadir a `cron` para que se inicie cuando arranca el sistema operativo el comando (es posible que se requiera añadir a la tabla del usuario sudo):

```bash
@reboot pigpiod
```
