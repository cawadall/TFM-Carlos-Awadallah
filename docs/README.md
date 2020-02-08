# Bitácora Periódica De Trabajo 

Este documento pretende ser una bitácora semanal de trabajo que recogerá los bocetos, diseños preliminares y prototipos y los progresos en el desarrollo de la Tésis de Fin de Máster "_Ejecución Mixta de Ejercicios de Visión Artificial y Robótica a través de la Web_". Se incluirá una entrada por semana, dispuestas en órden cronológico inverso (de más reciente a más antiguo) que hará las funciones de registro y cuaderno de notas, además de servir como herramienta para informar del estado del proyecto y recibir realimentación de manera más fluída.

---

## To Do:

- Reorganización eficiente de las capas Docker para reducir el tamaño de imagen. [**WIP**]
- Crear un API de conexión de Ejecución Mixta. [**WIP**]
- Incluir el soporte de robots reales para Windows y MacOS.
- Actualizar a ROS Melodic los nodos académicos.
- Ubuntu 18.04 [**DONE**]

## Semanas 45 a 47

Estas últimas semanas del proyecto completaremos la spruebas con grupos de voluntarios y sistemas diferentes. Probarmeos todos los supuestos de las tres vertientes de ejercicios: acceso a _hardware_ integrado, simulación y acceso a _hardware_ externo. Extraeremos parámetros de rendimiento y funcionamiento para validar la herramienta construida.

Por otro lado, dedicaremos gran parte del tiempo a la redacción de la memoria de la tesis, la cual iremos puliendo y mejorando hasta la fecha de defensa del proyecto. En este punto damos por finalizada la primera versión completa y funcional de la Ejecución Mixta.

## Semana 44

Con el _driver_ de Tello ya debidamente probado y arreglado, hemos implementado también el _back-end_ prototípico de un ejercicio destinado a al eejecución sobre el robot real del cliente. Esta infraestructura ha sido preparada de nuevo en forma de bucle de iteraciones que instancia una clase que contiene los métodos de envío de comandos a los actuadores y acceso a la informacón de los sesnores. La conexión con el dron se realizará a través de la red interna del cliente, por medio de un servidor de envío y recepción basado en UDP bajo una subred que levanta el propio robot.

Así, instanciamos una clase que contiene el _driver_ y la conexión y llamamos a sus métodos de control:

******************VIDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO***********

como se puede ver en el vídeo, tenemos ya soporte de robots reales incluso con el caso de robots con controladores caseros. Se tendrá que estudiar la posibilidad de inclusión de _drivers_ implementados or los clientes para sus propios robots al mecanismo de Ejecución Mixta.


## Semanas 42 y 43

Para completar los objetivos del proyecto, debemos incluir el soporte para robots reales. Hemos escogido el dron TELLo de DJI/INTEL dado que encaja a la perfección con el supuesto al que está orientado la Ejecución Mixta: robots de los que puedan disponer los usuarios medios. Se trata de un robot de "coste bajo" cuyo uso está muy extendido. Está dotado de estabilización visual y es muy ligeron con una autonomía relativamente extensa para los de su clase. Cuenta con dos cámaras integradas y es programable a través de Python.

Hemos dedicado estas semanas a la construcción de un _driver_ que nos permita controlar el dron no sólo a través de comandos de velocidad (usando las órdenes para las que está preparado este robot), sino también por posición. Además hemos incluido un método de reenvio de mensajes a través de una implementación casera de un mecanismo TCP (experimentamos la pérdida de algunos mensajes, en especial al controlar por posición, dado que el receptor del dron sólo soporta mensajes bajo canales UDP).

El _driver_ cuenta también con hilos de recepción de mensajes de texto, para acceder a los datos de batería, posición relativa, altura, estado, etc. y también para la recepción de vídeo. 

Hemos estado probando el controlador casero construido para el dron de manera local con pequeños programas compuestos por una declaración inicial y un bucle de instrucicones sencillas, de manera similar a como se implementará en forma de nodo en los cuadenrillos de los ejercicios que hemos construido para nuestra aplicaicón web.

## Semana 41

Dado el reciente éxito con las simulaciones, hemos dedicado esta semana a solventar un problema que llevábamos arrastrando unas semanas: los errores relacionados con el CORS (_Cross-origin resource sharing_). Básicamente, este tipo de errores se producen al tratar de solicitar recursos restringidos a un servidor desde otro servidor diferente desde el que se obtuvo el primer recurso, es decir, si se solicita en primera instancia la plantilla HTML de una página web a nuestro servidor y luego se solicita como parte del contenido de la misma los recursos de otro servidor como el de Jupyter o Gzweb. En algunos navegadores el motor de comunicación incluye ciertas cabeceras, como _Access-Control-Allow-Origin_ que rellenan con la información necesaria para "esquivar", este tipo de errores. Sin embargo, muchos otros no lo implementan ya que puede conllevar problemas de seguridad. Es por eso que la solución a estos errores suele recaer sobre la parte de servidor web. Por suerte, dado que el código de la aplicación nos pertenece, podemos establecer la configuración necesaria en nuestras respuestas HTTP:

```bash
Access-Control-Allow-Origin = "*"
```

De esta manera solucionamos los errores de CORS que obteníamos en especial del servidor de Jupyter localizado en la máquina del cliente web, dentro de su contenedor.

## Semana 40

Hemos completado el soporte de simulación y reconstruido la imagen de Ejecución Mixta para incorporar los nuevos cambios. En este punto disponemos de una herramienta multiplataforma que permite también simular robots:

******************VIDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO***********

De cara al lanzamiento de la nueva imagen, se hace necesario exponer también el puerto en el que correrá GzWeb, el cual hemos establecido de manera fija, para que la aplicación remota se conecte a él. También hemos tenido en cuenta la experiencia de usuario, mejorando los modelos de simulación y ocultando la bara lateral para evitar distracciones.

## Semana 39

Estos días se han dedicado a la construcción del _back-end_ del ejercicio del SigueLíneas con Fórmula 1. Se trata de un nodo académico en Python, construído bajo la misma filosofía iterativa que el ejercicio del Filtro de Color, que dispone tanto de los métodos de acceso a sensores y actuadores del robot (HAL API) como del establecimiento de los canles ROS de comunicación para poder enlazar el simulador con el código que se ejecuta en el cuadernillo. Esto es de alguna manera un mecanismo de intercomunicación que sucederá en el interior del contedor, pasando por el secuenciador. Los canales establecidos publican o se suscriben a los siguientes _topics_:

```
~$ rostopic list
/F1ROS/cameraL/camera_info
/F1ROS/cameraL/image_raw
/F1ROS/cameraL/parameter_descriptions
/F1ROS/cameraL/parameter_updates
/F1ROS/cmd_vel
/F1ROS/odom
/clock
/gazebo/link_states
/gazebo/model_states
/gazebo/parameter_descriptions
/gazebo/parameter_updates
/gazebo/set_link_state
/gazebo/set_model_state
/rosout
/rosout_agg
/tf
```

Hemos enriquecido este último para que pueda gestionar y redirigir adecuadamente los mensajes que provienen o van destinados a Gazebo. Así, desde el cuadernillo se instancia un objeto de la clase FollowLine() que incluirá este API de acceso y uso para controlar el robot de manera sencilla, y la simulación quedará lanzada también dentro del contedor de Ejecución Mixta y en constante comunicación con quien lo requiera a través de los canales anteriores.

## Semana 38

Ya hemos probado la Ejecución Mixta con cuadernillos que sólo requieren del uso de la CPU del cliente y con otro tipo de cuadernillos que requieren, además, de acceso a una cámara local. Esta semana la hemos dedicado a comenzar con la implementación del soporte de simulación.

Para ello, hemos incluído la versión 9 de Gazebo en el DockerFile del contenedor y hemos añadido el paquete de Gzweb (un interfaz web para el simulador Gazebo) que nos permitirá servir la interfaz de Gazebo a través de la web en un único _endpoint_ (conjunto ip:puerto) definido. También hemos enriquecido el secuenciador para pode rindicar qué simulación se debe lanzar. Para ello, hemos utilizado el método de organización de simulaciónes de ROS a través de LAUNCHERS (ficheros XML con extensión _.launch_) que nos permiten lanzar a la vez simulaciones con Gazebo y nodos que se comunican a través de ROS. Comenzamos a preparar el primer mundo de simulación: _f1_simplecircuit.launch_.

![FALTA IMAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEN********************](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/f1_simplecircuit.png)

Como se puede ver, se trata de un circuito de carreras con un robot F1 autónomo objeto de control. El ejercicio que plantearemos sobre esta simulación es el clásico Sigue-Líneas que tendrá por objetivo completar una vuelta al circuito sin perder la línea roja, con un simple control por desviación.

## Semana 37

Esta semana hemos finalizado la integración del servicio en producción y hemos aprendido a organizar, ubicar y parametrizar correctamente la aplicación en Django para entornos de producción. El resultado es que finalmente es posible acceder a la aplicación robótica en el dominio test.jderobot.org a través de la web, siempre y cuando se disponga de conexión de red, y testar la Ejecución Mixta de manera realmente remota.

![FALTA IMAGEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEN****************+](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/remote_server.png)

Paralelamente hemos completado el aislamiento del módulo orquestador del inicio de la Ejecución Mixta, al que hemos llamado secuenciador, a través de un ENTRYPOINT con parámetros de entrada que permite establecer qué herramientas se van usar, que aplicaciónes auxiliares se van a requerir y con qué ficheros de configuración o modelos se deben lanzar dichas aplicaciones.

## Semana 36

Continuando con la puesta en producción del servicio robótico, hemos implementado un recubrimiento del receptor de mensajes WebSockets con tecnología Daphne para que éste pudiese ejecutarse en la máquina como servicio (proceso en ejecución en segundo plano).

También hemos incluido Workers de Python para la gestión del paralelismo y evitar la concurrencia con los hilos de Python al recibir peticiones simultáneas.

Como ya se anticipó la semana pasada, la mayoría de los servicios web actuales se sirven bajo HTTPS porque pueden intercambiar información delicada (datos personales, contraseñas, cuentas bancarias,...). Es por eso que configuramos nuestra capa de seguridad con el protocolo SSL, para lo cual hacen falta certificados de clave simétrica. Tras unos días de investigación, encontramos la herramienta _Certbot_ (antiguo _Letsencrypt_) que nos permite obtener certificados gratuitos para nuestro sitio web. Esta herramienta promueve la web segura y gratuita, y por tanto se trata de software libre fácilmente instalable y manejable:

![Certobot](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/certbot.png)

Contiene una receta de instalación y uso que permite establecer el sistema en uso y la tecnología de servidor para obtener los certificados para nuestros dominios en un único paso:

```bash
sudo certbot --apache
```

## Semana 35

Con el la herramienta _middleware_ de Ejecución Mixta ya en una versión estable, hemos empezado a preparar el entorno de producción. a lo largo de esta semana hemos estduiado la tecnología de servidor HTTP [Apache](https://httpd.apache.org/) para sistemas Unix. A parte de por su robustez y por las herramientas de seguridad que proporciona, decidimos escoger esta tecnología al ser extensible, modular y de códgio abierto.

Comenzamos a preparar la primera versión del fichero de configuración del _Virtual Host_ de Apache bajo el que se servirá el sitio web de la aplicación docente que usa la Ejecución Mixta. En este caso, dado que queremos servir la página bajo el protocolo HTTPS (con una capa TLS de seguridad, encriptación), se han de preparar dos ficheros de configuración que declaren el sitio virtual para cada protocolo. Para el caso de HTTP, simplemente redirigimos al otro:

```bash
<VirtualHost *:80>

	ServerName test.jderobot.org

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/TFM-Carlos

	ErrorLog ${APACHE_LOG_DIR}/tfmcarlos/error.log
	CustomLog ${APACHE_LOG_DIR}/tfmcarlos/access.log combined


    Redirect / https://test.jderobot.org/


    RewriteEngine on
    RewriteCond %{SERVER_NAME} =test.jderobot.org [OR]
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]

</VirtualHost>
```

Algo que ha resultado vital para la depuración es la declaración de los ficheros de log de **Accesso** y **Error** en los que Apache registra diferentes eventos. Serviremos la aplicación bao el dominio test.jderobot.org, que apunta a la IP de una de las máquinas de la Universidad.

En cuanto a la configuración de la capa SSL sobre el _Virtual Host_, los bloques a declarar más importantes son los siguientes:

```bash
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        [...]

        ### Django configuration ###
        ############################
        ### Django statics ###
        Alias /static "/var/www/tfm-statics"
        <Directory "/var/www/tfm-statics">
            Allow from all
            Require all granted
        </Directory>

        ### Path to WSGI in Django project ###
        <Directory /var/www/TFM-Carlos/tfm_webserver/tfm_webserver>
            <Files wsgi.py>
                #Order allow,deny
                #Allow from all
                Require all granted
            </Files>
        </Directory>

        [...]

        ### Websocket ###
        ProxyRequests Off
        ProxyPass        "/_ws_/" "ws://127.0.0.1:8000/"
        ProxyPassReverse "/_ws_/" "ws://127.0.0.1:8000/"

        ### SSL ###
        SSLEngine on
        SSLCertificateFile       /.certs/fullchain.pem
        SSLCertificateKeyFile    /.certs/privkey.pem

        [...]

    </VirtualHost>
```
Destacar que para la capa SSL ha sido necesario indicar la ruta a los certificados y el puerto 443. Para la gestión del protocolo WS en producción simplemente redigiriremos el tráfico al servidor de websockets. Para la aplicación de Python sobre Apache (Django) se indica la ruta del fichero de aplicqación WSGI y la ruta de almacenamiento seguro d elos ficheros estáticos del servicio.

## Semana 34

Aunque esta semana estaba planeado la migración de la herramienta de Ejecución Mixta a un entorno de producción del servicio, este objetivo se retrasará debido a algunas mejoras en el procesamiento de la ejecución local y su estado que deben introducirse al considerarse necesarias para expandir la capacidad de generalización, como puede ser el robustecer el intercambio de datos multimedia contenidos en los cuadernillos (imágenes o vídeos, además de texto y _widgets_, que deben ser codificados debidamente antes de la transmisión), o tratamiento y contención de excpeciónes que se produzcan en situaciónes inesperadas (cuadernillos vacíos o no decodificables, etc.)

Se ha puesto mucho énfasis en extender el protocolo de mensajería de la Ejecución Mixta  para que sea capaz de lidiar con diferentes códecs de audio, vídeo e imágenes como flujo de bytes al transmitirse por la web, en tanto que esta codificación es mucho más sensible y variante que la utilizada para intercambiar texto (mediante ASCII o UTF-8, principalmente). La transformación más utilizada ante contenido de naturaleza más compleja en el mencanismo de comunicación de esta herramienta (principalmente testado con contenido _.csv_, _.mat_, _.png_, _.jpg_, _.mp4_ y _.gif_) es la transformación de los hipotéticos datos multiconteido a un flujo **Base64**, realizada en función de la extensión del fichero que los contiene. Se obtiene un problema similar en la recogida del código cuando finaliza el proceso de Ejecución Mixta, ya que este puede a su vez contener imágenes empotradas principalmente, además de otros tipos de contenido. Este problema se tratará también con la transcodificación propuesta.

Se testo esta funcionalidad con cuadernillos diseñados para tareas de tratamiento digital de imágenes, con otras estructuras complejas de datos además de imágenes, como se muestra en los siguientes vídeos:

##### [YOUTUBE VIDEO] Mixed Execution Testing with First TDI Practice
[![TDI_practice1](https://img.youtube.com/vi/6VyEktlbWdM/0.jpg)](https://www.youtube.com/watch?v=6VyEktlbWdM "")

##### [YOUTUBE VIDEO] Mixed Execution Testing with Second TDI Practice
[![TDI_practice2](https://img.youtube.com/vi/MOYrnSbF818/0.jpg)](https://www.youtube.com/watch?v=MOYrnSbF818 "")

Paralelamente seguimos ampliando la funcionalidad del servicio web, con el fin de demostrar la integración de la Ejecución Mixta con una aplicación completamente funcional y válida. En este caso, se incluyó la capacidad de servir cuadernillos personalizados, por ejemplo con el progreso hecho en visitas anteriores a la aplicación.

## Semana 33

En la búsqueda de la mejora de usabilidad y experiencia de usuario, esta semana hemos prescindido de la parametrización del puerto en el que escucha el canal de Ejecución Mixta (concretamente el secuenciador), estableciendo uno por defecto, aunque manteniedo la posibilidad de especificar otro. Esto no interfiere en el despliegue y es ransparente para el usuario, pero le libera de la decisión de escoger un puerto, especialmente si desconoce los puertos libres de su máquina o si siente inseguridad en lo relativo a la gestión de sistemas. Hemos elegido un puerto que rara vez se usa en las máquinas finales, reservado para tareas de desarrollo o prestado de servicios (8888). Modificamos el UI de la aplicación para proporcionar acceso al menú de configuración del canal a través de un botón, pero la aplicación seguirá utilizando el mismo API.

En cuanto al cuadernillo que hemos estado utilizando como ejemplo, se encontraron algunos problemas en la utilización de la extensión _init\_cell_ en conjunción con la creación de _widgets_ en el cuadernillo, debido a conflictos en el orden de carga de las extensiones y los _widgets_. Estudiaremos como cambiar ese orden a nuestra conveniencia. Entre tanto, hemos mejorado el interfaz a través de visores web. Esto nos permitirá añadir más adelante a la Ejecución Mixta el manejo de _WebSockets_, que se ha planeado utilizar para enviar imágenes a los visores de la web desde la ejecución en el contenedor del cliente.

Empezaremos a estudiar también la sintaxis de Docker y BASH para automatizar la construcción que hemos hecho manualmente de la imagen a través de un DOCKERFILE con una configuración inicial para el secuenciador de Ejecución Mixta contenido en un ENTRYPOINT que prepare el entorno para la aplicación concreta.

## Semana 32

Dada la exetensión de funcionalidad de los cuadernillos (de los que disponemos actualmente, y los potenciales) a través de extensiones de Jupyter, hemos estudiado como habilitar el uso de dichas extensiónes dentro del contenedor en que el servidor de Jupyter se ejecuta.

También hemos investigado acerca del estado del soporte de Docker sobre otros sistemas operativos, especialmente MacOS (estructuralmente bastante parecido a linux) y Windows (diametralmente opuesto) debido a la intención inicial de lograr una herramienta robótica multiplataforma. A falta de realizar test más exhaustivos, hemos concluído que el soporte actual está limitado para las distribuciónes _Windows 10 Pro_ y _Enterprise_ del SO de Microsoft por un lado, y que en MacOS el principal obstáculo radica en el acceso al _hardware_ conectado por USB, el cual es bastante limitado para aplicaciónes desconocidas. Seguiremos indagando y, en cualquier caso, dejaremos la puerta abierta para abordar el problema en cuanto esta situación cambie.

## Semana 31

Lanzamos ya esta semana el tercer prototipo, ya en versión beta, de la Ejecución Mixta. El lado cliente web está preparado con una imagen docker que pone a funcionar el servidor de Ejecución Mixta y todos los módulos auxiliares necesarios para la aplicación, contenidos en el propio docker o enviados en tiempo de ejecución al mismo (entre lo que destaca Jupyter y sus extensiónes, las librerías OpenCV, el simulador, los _drivers_, ...) y que garantiza el acceso al _hardware_ local (CPU y GPU). Aquí hay un vídeo demostrativo:

##### [YOUTUBE VIDEO] Mixed Execution Testing with Docker-Based Client side
[![mixed execution docker](https://img.youtube.com/vi/KlgqdIBA4TE/0.jpg)](https://www.youtube.com/watch?v=KlgqdIBA4TE "")

El token de acceso para la autenticación del servidor de Jupyter ha sido eliminado para mejorar la experiencia de usuario, eliminando así la dependencia de que el usuario copiase a mano el _string_ generado durante la iniciación de la herramienta. Dicho token puede eliminarse dados los mecanismos ya de por sí poco permisisvos que hemos implementado en lo relativo a la seguridad de la ejecución, sumado al hecho de que gracias al contenedor el servidor se encuentra en un entorno aislado en el que el mayor problema posible que puede surgir sería tratado simpelmente parando y eliminado el contenedor y levantando uno nuevo, todo en un sencillo paso (`docker stop <contenedor> && docker start <contenedor>`). La máquina del cliente no puede verse en ningún caso afectada.

## Semana 30

La conectividad de red con el Docker del cliente ha sido verificada desde la máquina que actúa como _host_ de la aplicación, además del acceso a la cámara local del cliente en una primera aporximación al acceso _hardware_ específico. Para esto último se añadió algunos _flags_ al comando de inicialización de la herramienta para solicitar el mapeo de las interfaces que correspondan entre el contenedor y la máquina sobre la que se ejecuta. Verificamos este acceso a través de las utilidades que forece OpenCv para el acceso a una webcam:

```python
import cv2
print(cv2.VideoCapture(0).isOpened())
```

Para que la Ejecución Mixta sea capaz de conectar el cliente con la aplicación remota es necesario lanzar una instancia de servidor Jupyter dentro de dicho contenedor, pero a la vez garantizar su acceso desde fuera, concretamente desde la interfaz de usuario de la web servida por la máquina que contiene la aplicación robótica. También se ha de mapear debidamente los puertos en los que las herramientas internas del contenedor (entre ellas este servidor de Jupyter) esperan recibir o enviar datos. Aún así, existen algunos problemas a tratar en lo que se refiera a la copia de ficheros que provienen del exterior del contenedor, relacionados con los permisos de gestión y las políticas de Jupyter. Los próximos pasos irán en esta dirección.

También hemos revisitado la psibilidad de reemplazar el token de autenticación de jupyter por una _cookie_ con la misma información, a la que se acceda automáticamente (el _browser_) sin requerir interacción. Sin embargo las políticas de CORS no permiten la consulta, modificación u obtención de _cookies_ fijadas por otros dominios (en este caso aquel bajo el que se sirve Jupyter). Tambień se estudió la posibilidad de incluir código JS en el interior del _iframe_ con la intención de que fuera ejecutado en ese otro dominio dependiente, corriendo la misma suerte. Hemos aprendido que la web es muy robusta (¡y menos mal!) ante los intentos de acceso o ejecución de cosas desconocidas.

## Semana 29

Una vez el servidor con la aplicación ha sido levantado, el lado dliente se prepará de tal manera que la Ejecución Mixta funcione a través de la imagen instalada. La intención es que los usuarios que acceden a la aplicación robótica no deban instalar ninguna herramienta, sino que serán provistos de la imagen docker de manera muy simple que les ahorrará ese proceso de instalación y puesta a punto. Por ello, esta imagen será extendida en los próximos días con aquellas herramientas que más se utilizan en el campo de la robótica, además de otras de nuestra elección cuya utilidad se vió durante el proceso de investigación (servidor de WebSockets, extensiones de Jupyter).

Por otro lado, pasaremos una serie de test para verificar que el contedor permite el accedo a la webcam local, que tiene conectividad de red actuando como una subred de aquella en la que está contenido y también que hay acceso al _hardware_ "externo", conectado a través de puertos USB. Con ello, podremos preparar entornos (en forma de ejercicios) que nos permitan probar la Ejecución Mixta con  cámaras integradas e incluso interfaces de robots reales de los que disponga el cliente.

## Semana 28

En tanto que la tecnología de Ejecución Mixta está funcionado en este punto (como segundo prototipo), es el momento de enriquecer la parte de servicio (aplicación robótica) para que requiera más potencia de ejecución a través de tareas más exigentes. Hemos enriquecido las bases de datos, modelos y clases de Python para que nos permitan ampliar la funcionalidad de los ejercicios, y hemos retocado el interfaz para que exija actualizaciónes constantes del estado del simulador y la ejecución al canal de Ejecución Mixta, con lo que se consigue un servicio fluído y usable.

Empezamos a estudiar los mecanismos de publicación de la imagen Docker para poder difundirla cuando esté terminada, dado que la naturaleza de este proyecto es _software_ libre.

## Semana 27

Hemos estudiado el uso que Google hace de la extensión que incluye en Jupyter para el manejo del protocolo de _WebSockets_ en su versión de la "Ejecución Local para _DeepLeraning_". En principio, parece que esta extensión únicamente cumple la función de realizar un cambio de protocolos de manera limpia (hay limitaciones en el cambio de protocolos de una comunicación ya establecida en la web) una vez se ha iniciado la conexión (HTTP(S) -> WS) y por lo tanto su uso en nuestro caso puede ser descartado en tanto que no necesitamos realizar ese cambio, con lo que reducimos también las dependencias que el cliente debe instalar a practicamente cero en este punto.

Hemos puesto énfasis esta semana en temas de seguridad, concretamente en garantizar la integridad del código de la ejecución a través de la ofuscación. Estudiamos maneras de ofuscar y minimizar el código JavaScript encargado de la comunicación (usando el API) entre el contenedor del cliente y la aplicación remota (Servidor Jupyter <--> Browser). La herramienta más prometedora hasta el momento es [esta](https://obfuscator.io/), dado que es parametrizable para adaptarse al caso de uso más conveniente. Indagaremos más.

## Semana 26

Debido a los problemas que surgieron en las últimas pruebas, hemos cambiado parcialmente el enfoque del problema:

A partir de este punto, utilizaremos el _browser_ del cliente como intermediario entre el servidor web remoto y el Servidor de Jupyter situado en el cliente web. Básicamente, el navegador actuará ahora como un _proxy_ redirigiendo los mensajes generados en el servidor web como si él fuera el origen. Con ello, conseguimos atravesar los tediosos problemas de seguridad de la comunicación con la máquina del cliente, en tanto que al origen ahora es conocido. sin ambargo, ha sido necesario realizar múltiples cambios al servidor de prueba y al protocolo de comunicaciónes principalmente, dado que es necesario que el servidor envie en un primer paso todo el código necesario al _browser_, además de cambiar el lenguaje utilizado para la comunicación a JavaScript. La accesibilidad se mantiene dado que este es el lenguaje estándar en los navegadores web.

En este caso ambos tests, el primero con comunicación UC3M -> URJC y el segundo con entorno MI CASA -> URJC pasaron como se había planificado. Un ejemplo de esta prueba puede verse en:

##### [YOUTUBE VIDEO] Prototype of Mixed Execution Through Networks.
[![mixed execution prototype](https://img.youtube.com/vi/IsNA5rBRBsA/0.jpg)](https://www.youtube.com/watch?v=IsNA5rBRBsA "")

## Semana 25

Dado el éxito en el test de utilización de diferentes máquinas actuando como cliente y servidor, es el momento de diseñar un test en el que el cliente web esté ahora detrás de un NAT y un _firewall_, es decir, en una red siferente a la del servidor, como pasaría en un entorno real de usuarios que acceden a un servicio.

En este caso, las peticiónes y comandos que la aplicación web envía al Servidor de Cuadernillos de Jupyter tienen que atravesar los mecanismos de seguridad establecidos para mensajes procedentes del exterior. Sin abrir los puertos necesarios para la comunicación en la máquina del cliente, esta prueba fracasó. Estudiaremos detenidamente el escenario y el proceso para aislar el error y tratar de ponerle remedio.

También estudiamos el código de la extensión de Google en búsqueda de ideas. Además, seguimos trabajando para solucionar el problema de la _cookie_. Por último, agrupamos el código de los ficheros de _back-end_ del Cuadenrillo de test (_Color Filter_) en un único _script_ de Python. También se estudió la minimización de ese código para aligerar el tráfico entre el servidor de la aplicación y el cliente a través de la web.

## Semana 24

Plantemos el test del primer prototipo de Ejecución Mixta utilizando diferentes máquinas en lugar de tener _host_ de la aplicación y cliente en la misma. Para ello, una primera máquina se encargó de ejecutar el servidor a través de la tecnología Django que esperará a la petición del cuadernillo del _Color Filter_ que se adaptó la semana pasada. Una segunda máquina, en la que correrá el Servidor de Jupyter, se conectará como cliente a dicha aplicación, solicitará el ejercicio  y esperará a recibir órdenes generadas por la aplicación para obtener, ejecutar, modificar y reenviar el Cuadernillo en base a la interacción con el usuario humano. Una demostración de la Ejecución Mixta entre dos máquinas puede verse en el siguiente vídeo:

##### [YOUTUBE VIDEO] Mixed Execution Testing with Two Machines
[![mixed execution 2 machines](https://img.youtube.com/vi/nGDd6HG124s/0.jpg)](https://www.youtube.com/watch?v=nGDd6HG124s "")

Dado que la implementación acual depende del envío de un conjunto de ficheros de código y configuración que dan soporte al ejercicio, hemos empezado a estudiar maneras de minimizar código Python.

## Semana 23

Para probar el mecanismo de Ejecución Mixta implementado, esta semana se ha centrado en adaptar el cuadernillo _Color Filter_ para que se conecte a la webcam disponible por defecto y opere de manera normal en la máquina del cliente. Esto incluye el envío de los ficheros de _back-end_ del ejercicio, para lo cual se ha experimentado con diferentes mecanismos, entre los que destacan: el uso del REST API con el formato que corresponda, los mecanismos de importación web de bibliotecas de Python y los sistemas de empaquetdado de ficheros en este lenguaje. Por ahora, se concluye que la mejor opción es continuar con el REST API, aunque revisaremos las otras opciones más adelante.

De manera adicional, hemos estudiado el mecanismo de sesiónes de Django para tratar de reemplzar el token (manual) de autenticación por la _cookie_ que el servidor de Jupyter establece en el navegador al arrancar. La intención es sustituir el token por la información de la _cookie_ para aumentar la automatización del proceso.

## Semana 22

Creamos una serie de experimentos para verificar que el _kernel_ que ejecuta el código es el adecuado (aquel que fue iniciado remotamente en el Servidor de Cuadernillos del cliente). Entre las pruebas está la interrupción del _kernel_ del cliente, con la que se comprobó que el código del cuadernillo que se mostraba en la web ya no podía ser ejecutado, y ni siquiera se podía interaccionar con él. El próximo test se enfocará ya al caso de disponer de dos máquinas en comunicación.

También implementamos un mecanismo de recogida del código retocado por el usuario para verificar el funcionamiento bidireccional de la comunicación. El servidor de pruebas realizará una solicitud al _kernel_ del cuadernillo cuando el cliente haya hecho cambios (detectados a través de escuchadores de eventos en el _iframe_) o cuando se solicite expresamente por el usuario (guardar código). Así, la aplicación solicitará al servidor de Cuadernillos de Jupyter la última versión del cuadernillo del ejercicio y lo almacenará.

##### [YOUTUBE VIDEO] Mixed Execution (Remote Web Server + Local Notebook Server + Local Kernel) FIRST VERSION
[![mixed execution 2](https://img.youtube.com/vi/2BqTAunmx30/0.jpg)](https://www.youtube.com/watch?v=2BqTAunmx30 "")

Entretanto, seguimos investugando el uso de las _cookies_ del navegador. Las [sesiónes](https://docs.djangoproject.com/en/2.1/topics/http/sessions/) de Django pueden resultar útiles.

## Semana 21

El siguiente paso es iniciar remotamente (a través de mensajes procedentes del servidor web) una sesión de Jupyter y un _kernel_ asoaciado al cuadernillo que se ha enviado. Usamos otras de las operaciónes del REST API (debidamente configurada) enviadas a las rutas apropiadas para establecer la conexión.

Con fines depurativos y para verificar el funcionamiento y la ejecución del código por el _kernel_ que se ha lanzado en el cliente, estudiamos las maneras de embeber el Cuadernullo en la web que sirve el servidor de test. Puede que sea necesario reconfigurar los ficheros del servidor de Jupyter para modificar convenientemente los mecanismos de seguridad (XSRF, principalmente) del serivdor con tecnología Tornado subyacente, en tanto que el entorno ahora es distinto. Nos centramos en el uso de `<iframes>`.

En este punto, todos los agente involucrados se inicial crrectamente y el _kernel_ parece estar preparado para recibir órdenes y peticiones de ejecución asociadas con el código del cuadernillo que se encuentra en la web.

## Semana 20

Se ha construido la primera versión del servidor de pruebas en Django. Este servidor simplemente espera a recibir solicitudes, y cuando recibe una de tipo "empezar ejercicio" simplemente sirve el cuadernillo apropiado (aunque en este punto sólo existe uno) a través del REST API de Jupyter a un _kernel_ que el suaurio debe lanzar (en este caso, en un puerto distinto al del servidor).

![TEST SERVER](https://github.com/cawadall/TFM-Carlos-Awadallah/blob/master/docs/img/TEST_SERVER.png)

A través de la operación POST y colocando la ruta adecuada, el cuerpo del mensaje HTTP debidamente rellenado y con las opciones correctas de seguridad en las cabeceras (principalmente el token que el Servidor de Cuadernillos de Jupyter establece para la autenticación y creación de sesiones de usuario), conseguimos que el _kernel_ reciba el cuadernillo:

![POST](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/POST_REST_API.png)

Ahora debemos investigar las opciónes para la solicitud y envío del resto de ficheros de código en los que se basa el ejercicio (su cuadernillo). También estudiaremos si exitse la posibilidad de sustituir el token de autenticación por _cookies_ que el Servidor de Jupyter establecen en el navegador.

## Semana 19

Hemos empezado a trabajar en un Servidor de Test. Exploramos dos rutas:

- Abrir los puertos que utiliza el contenedor docker en el cliente, de tal manera que pueda utilizarlo (Gazebo + GzWeb + Notebook Server + Jupyter Kernel). La aplicación, que originalmente tiene el código que el usuario solicita, lo envia a través de SCP al docker de la máquina cliente. Esto funciona, pero no resulta elegante solicitar a los usuarios (que pueden no tener conocimientos técnicos) que abran sus puertos, además de las claras implicaciónes de seguridad.

- Colocar Servidor de Cuaernillos y Kernel en el lado cliente. El servidor remoto (web) envía el cuadernillo al directorio sobre el que corre el servidor de Jupyter (local) y luego le envía órdenes al _kernel_ para que funcione con normalidad. Para ello, necesitamos comprender el API HTTP que utiliza el Servidor de Cuadernillos de Jupyter (en búsqueda de operaciónes que digan, por ejemplo, "toma este cuadernillo"). Sospechamos que sea necesario inciar una comunicación HTTP del web server al _browser_ y una conexión _WebSockets_ del _browser_ al Notebook Server.

Dado que la segunda opción es más interesante, estudiamos el [REST API](https://github.com/jupyter/jupyter/wiki/Jupyter-Notebook-Server-API), que contiene algunas opciónes que nos pueden resultar úriles.

![REST API](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/REST_API.png)

## Semana 18

Terminamos de estudiar las trazas que el código de Jupyter imprime para saber qué esta pasando durante el establecimiento de la comunicación. También estudiamos la  [extensión](https://github.com/googlecolab/jupyter_http_over_ws/blob/master/jupyter_http_over_ws/handlers.py) de Colaboratory para embeber la comunicación HTTP en el protocolo _WebSockets_ para luego conseguir evitar problemas con los _firewalls_ de los usuarios dado que la infraestructura de Jupyter permite el uso de este protocolo para empaquetar los mensajes ZMQ.

Estudiamos también la posibilidad de instalar el proyecto Jupyter desde código fuente (en luhgar de a través de paquetes debian) para cambiar los ficheros principales por otros ligeramente extendidos que incluyan más mensajes de control con el fin de observar claramente qué sucede en cada paso. También empezamos a indagar en otros mecanismos como el REST API de Jupyter.

## Semanas 16 y 17

Ahora es momento de profundizar en la distribución de Jupyter y su estructura a través de los ficheros accesibles desde el navegador (_session.js_ y _kernel.js_ principalmente) para tratar de entender por completo el mecanismo y encontrar las herramientas que nos permitan alcanzar el objetivo de los _local runtimes_ on entornos de ejecución locales para Cuadernillos de Jupyyer.

Hemos utilizado _sniffers_ para monitorizar la comunicación entre el servidor de Colaboratory y el _browser_, y también entre éste y el _kernel_ local para comprobar como se resuelve dicha comunicación (incluyendo HTTP y _WebSockets_).

He subido los recursos que utiliza el Cuadernillo a [este directorio](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/) para que estén accesibles para cualquier usuario en cualquir sitio sin tener que descargarlos. Estos recursos se moverán al disco del servidor de la aplicación en cuanto esté construida una versión funcional.

# Semana 15

Seguimos investigando la infraestructura de Colaboratory para adaptar el cuadernillo del ejercicio de tal manera que funcione con normalidad en el servidor de Google, permitiendo el bucle de visualización. Además, hemos eliminado el uso de _widgets_ integrados en el cuadernillo debidoa que la versión actual de Colaboratory no ofrece soporte para ellos (no soporta _custom messages_) y sólo dispone de algunos _widgets_ creados específicamente para la plataforma, idóneos para Machine Learning pero prácticamente inútiles en otros ámbitos como el que nos ocupa. La posibilidad de incluir botones en el _front-end_ se estudiará. Este es el resultado de la ejecución de un Cuadernillo a través de una conexión mixta:

##### [YOUTUBE VIDEO] Mixed Execution (Remote Server + Local Kernel) Through Google Colaboratory
[![mixed execution](https://img.youtube.com/vi/oF6kp_x16M4/0.jpg)](https://www.youtube.com/watch?v=oF6kp_x16M4 "")

Centraremos los esfuerzos en comprender las sesiónes y los _kernels_ que jupyter usa para la mensajería, con el fin de extraer la información de conexión (URL) de un nuevo _kernel_ local y conectarse a él desde el navegador.

## Semana 14

Esta semana nos enfocamos en mejorar la infraestructura del ejercicio sobre el que se contruirá la aplicación robótica, tratando de conseguir que la visualización se organice según un bucle iterativo (de tal manera que se pueda crear comportamientos reactivos) con capacidad de control en base a una serie de botones de parada, pausa y arranque, a la par que la posibilidad de habilitar o deshabilitar la visualización. Esto nos permitirá probar la potencia de Jupyter y con ello podremos saber si el alcance de esta herramienta es suficiente para la construcción de aplicaciónes robóticas, que serían el "interlocutor" de la herramienta de ejecución compartida que se quiere construir.

Para los controles hemos profundizado en los [_widgets_ de Colaboratoy]((https://colab.research.google.com/notebooks/widgets.ipynb). Una feractorización de la infraestructura del cuadernillo es necesaria para introducir estos cambios.

## Semana 13

La primera aproximación a la solución del problema pasa por estudiar la solución de Google Colaboratory, que si bien no es nuestro caso exacto, debe contener etapas comunes en tanto que se comparte un elemento _hardware_ específico. Hemo subido un Cuadernillo que hemos creado a su servidor como prueba, y hemos usado sus mecanismo de conexión a un entorno de ejecución local o [_local runtime_](https://research.google.com/colaboratory/local-runtimes.html).

![local_runtimes](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/local_runtimes_colab.png)

Para tratar de hacernos una idea de su comportammiento, hemos utilizado WireShark para capturar el tráfico en la interfaz de _loopback_ del sistema en el que se hizo la prueba, filtrando el tráfico por el puerto en el que se lanzó el _kernel_ que conforma el entorno local al que el servidor de colab se conecta.

![wireshark](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/wireshark_localruntimes.png)

En un intento d eobtener más información, realizamos algunas pruebas como el intento de inicialización del entorno local sin haber levantado el _kernel_ o como tirar el _kernel_ en medio de una sesión, pero no obtuvimos resultados concluyentes: la aplicación estaba preparada para tales situaciónes y no mostraba comportamientos extraños que pudieran sernos útiles, simplemente se reconectaba a un entorno de ejecución remota, haciendo uso de uno de los servidores de sus granjas de ordenadores.

También dedicamos gran parte del tiempo al estudio de la comunicación que se produce entre el Servidor de Cuadernillos y el _Kernel_ de Jupyter medianta la documentación oficial del proyecto y del protocolo de comunicaciónes que usan.

## Semana 12

Es necesario explorar posibles maneras de conseguir que el cuadernillo, almacenado inicialmente en un servidor remoto, ejecute el código que contiene usando el _hardware_ local del cliente que accede a él (_Kernel_ local de Jupyter). 

Hemos visto que esto es en cierto modo posible gracias a los [entornos de ejecución local](https://research.google.com/colaboratory/local-runtimes.html), así que empezaremos a trabajr esta idea. Se ha visto que, para hacerlos funcionar, es necesario incorporar una extensión al _kernel_ de Jupyter, habilitarla, y reemplazar el protocolo ZeroMQ encargado de la comunicación entre el _front-end_ de Jupyter y los _kernels_ que se levantan por una solución tecnológica que nos permita "engañar" al _browser_ local de tal manera que cierto contenido procedente del servidor remoto sea aceptado por el servidor de Jupyter, más concretamente reconocido por el _kernel_ local, con lo que el Servidor de Cuadernillos se conectaría al navegador y este al _kernel_ de Jupyter.

En un principio, creíamos que [este script](https://www.npmjs.com/package/@jupyterlab/services) podía resolver parte de la funcionalidad, así como otros ficheros contenidos en [este repositorio](https://github.com/jupyterlab/jupyterlab/tree/master/packages/services). Tras un estudio detallado del mismo quedó descartado. Sin embargo, su estudio no fue en vano, pues al ser un repositorio oficial enlazado al proyecto Jupyter pudimos entrever parte del mecanismo subyacente.

Los próximos días se terminará de estudiar estos recursos para extraer la mayor cantidad de información posible y poder comenzar a trabajar en la idea de la ejecución compartida (mixta). El objetivo principal a medio plazo en llegar el entorno completo de ejecución local del cuadernillo del filtro de color (Color Filter).

## Semana 11

Hemos hecho algunas mejoras en relación a la experiencia de usuario, como eliminar la salida de las celdillas cuando el usuario pulsa sobre cualquiera de los botones implementados, de tal manera que no se ven forzados a reiniciar el _kernel_ en el proceso de escritura del código y de depuración. También hemos cambiado los dos botones de "_Play Code_" y "_Pause Code_" por un único botón conmutable, que lo simplifica: 

![playtoggle](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/playtoggle.png)

![pausetoggle](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/pausetoggle.png)

Casi tenemos preparado el primer ejercicio y podemos pasar a la parte más interesante del proyecto, en la que se tratará de construir una aplicación robótica que sirva el ejercicio diseñado, y una herramienta que sintonice ambas partes, cliente y servidor, para compartan una ejecución convenientemente en la que no se quiera mucho consumo de recursos en el lado servidor.

Paralelamente hemos destinado parte del tiempo a investigar algunas otras herramientas para enriquecer el ejercicio con mayor funcionalidad y dotarlo de mayor intuitividad, haciéndolo más parecido a un caso real, lo que también se quiere alcanzar con este proyecto. Estas herramientas son principalmente:

- JupyterLab
- Extensiones de Jupyter

## Semana 10

Para simplificar la interacción con el ejercicio y permitir la pausa académica y la interrupción del códigom hemos añadido botones con eventos que se asocian a las acciones incluídas la semana anterior, a través de _widgets_ interactivos que permiten al usuario realizar estas acciones, además de habilitar y deshabilitar la visualicación de las imágenes a voluntad.

Mejoramos también el bucle de visualización para ofrecer umágenes cada segundo, y también incluyendo mensajes de aviso si no se ha establecido una imagen filtrada para visualizar, por ejemplo.

##### [YOUTUBE VIDEO] Buttons for Play, Pause and Visualization On/Off
[![buttons](https://img.youtube.com/vi/00w6aofU95A/0.jpg)](https://www.youtube.com/watch?v=00w6aofU95A "")

## Semana 9

Hemos diseñado un bulce de visualización de imágenes que aprovecha la naturaleza iterativa del método que ejecuta el algoritmo del ejercicio (introducido hipotéticamente por un usuario). Este bucle está basado en el sampleo periódico (cada 3 segundos, por limitaciónes de latencia y _jitter_) del flujo de salida de imágenes resultante del procesado que al algoritmo realiza sobre el flujo de vídeo entrante procedente de alguna cámara. Con ello, extendimos también el set de herramientas de depuración del ejercicio:

##### [YOUTUBE VIDEO] Visualization Loop printing filtered images each 3sec
[![visloop](https://img.youtube.com/vi/BBZKI12Hxtg/0.jpg)](https://www.youtube.com/watch?v=BBZKI12Hxtg "")

Por otro lado, añadimos también la "Pausa Académica", a través de la cual se consigue facilitar al usuario el proceso de codificación de la solución, en tanto que se adopta una filosofía de "Programación en Vivo" con la presencia de herramientas que permiten al usuario detener y reanudar la ejecución de su algoritmo, por ejemplo para realizar cambios sobre él y ver cómo se materializan esos cambios sobre el flujo entrante. Esto evita que tenga que reiniciarse el _kernel_ con cada cambio realizado para cargarle un nuevo código. El funcionamiento se puede ver en el siguiente vídeo:

##### [YOUTUBE VIDEO] Academic Pause
[![academicpause](https://img.youtube.com/vi/lGeGHJZUxpY/0.jpg)](https://www.youtube.com/watch?v=lGeGHJZUxpY "")

## Semana 8

Como parte del proceso de refinado de la visualización y la interacción con del Cuadernillo ColorFilter en Jupyter, hemos encontrado y testado una serie de herramientas sin relación oficial con el desarrollo de IPyhton que permiten ampliar la funcionalidad de los Cuadernillos. Estas extensiones están en su mayoría escritas en lenguaje JavaScript y serían cargadas e iniciadas directamente el navegador del cliente (local). Estas herramientas se llaman [nbextensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions).


El enlace superior contiene una pequeña descripción del repositorio y las extensiones, una receta de instalación y una guía de uso. Hemos instalado el proyecto como se mostraba y probado las extensiones disponibles. De entre todas hemos visto especial potencial en dos de ellas: _Initialization Cell_ y _Hide Cell_. Una vez finalizada la instalación se puede acceder a ellas incluso de forma gráfica en la barra de herramientas de la sección _tree_ del interfaz de Jupyter, por lo que tienen  muy buena integración con la plataforma.

![nbextensions](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/nbextensions1.png)

---
En cuanto a la extensión _Initialization Cell_, puede habilitarse a través del configurador de extensiónde de Jupyter, [jupyter_nbextensions_configurator](https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator):

![jupyter_nbextensions_configurator](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/nbextensions2.png)

En función del sistema en el que se intenten habilitar, se puede encontrar problemas de falta de permisos. En tal caso, pueden habilitarse haciendo uso de un terminal, con:

```bash
sudo jupyter nbextension enable init_cell/main
```

Una vez habilitada, se añaden las barras de herramientas asociadas a esta extensión del siguiente modo:

![toolbars](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/nbextensions5.png) 

y se accede a esta barra de herramientas en cada celdilla que se quiera establcer como celdilla de inicialización cuyo código se ejecutará según se cargue el cuadernillo. Así, se marcaría como "_initialization cells_" las celdillas deseadas como se muestra:

![checkbox](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/nbextensions3.png)

---
De manera similar a la anterior, hay otra extensión que permite ocultar las celdillas que se marquen, esta es _Hide Cell_. En conjunto con la anterior, podemos añadir al cuadernillo funcionalidad adicional sin que el código que la genera o gestiona aparezca visible en el cuadernilo, por ejemplo, podremos añadir botones ricos en acciones cuyas declaraciónes no estén visibles. De nuevo, hay que habilitar esta extensión con:

```bash
sudo jupyter nbextension enable hide_input/main
```

Después, como se muestra [aquí](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/hide_input/readme.html), tendremos que marcar aquellas celdillas que queramos ocultar. Se ha hechomodificando los metadatos de las celdillas en cuestión: 

![metadata](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/nbextensions4.png)

---
El resultado es el siguiente: 

THE RESULT IS THE FOLLOWING:
##### [YOUTUBE VIDEO] Result of the extensions 'Initialization Cells' added to Color Filter Notebook.
[![extensions](https://img.youtube.com/vi/e2_fgAAeLx4/0.jpg)](https://www.youtube.com/watch?v=e2_fgAAeLx4 "")

## Semana 7

Empezamos a investigar maneras de enriquecer la visualización del ejercicio del Filtro de Color. Además, esta semana hemos puesto mucho esfuerzo en localizar, analizar y probar las herraientas robóticas de moda y cuyo uso está mas extendidas, para así filtrar aquellas que utilizaremos más adelante. Hemos decidido hacerlo en este punto dado que es importante evaluar la integración de Jupyter en el mundo de la robótica, y decidir si es viable continuar con esta plataforma como corazón de la idea del mecanismo de ejecución mixta, en función de si podemos construir a su alrededor.

En principio, hemos tenido éxito en tal búsqueda, pues la practica totalidad de herramientas estudiadas y seleccionadas eran de una u otra manera compatibles con Jupyter, auqnue hubiera que construir mecanismos de enlace. Las principales herramientas en las que se apoyará esta idea son, de momento, las siguientes: GzWeb, Jupyter, Docker, OpenCV, WebSocketsServer y JdeRobot.

## Semana 6

Empezamos a dar los toques finales al _back-end_ del ejercicio del ColorFilter asumiendo que los componentes necesarios (cámara) se ejecutan en modo local. Estudiamos también las posibilidades de acceso a la cámara, principalmente mediante las funciones del sistema operativo, pero también mediante las librerías OpenCv e incluso a través de herramientas web, para más adelnate seleccionar la más conveniente. De momento, hemos optado por las funciones de las librerías de procesamiento digital.

## Semana 5

Seguimos probando la solución colaboratory de Google. Estudiamos su API, trazamos el guión de operaciones que parecen estar sucediendo y localizamos la fuente de código que creemos que gestiona el proceso aunque, por supuesto, aparece ofuscada. Seguiremos indagando.

## Semanas 3 y 4

Comenzamos a esbozar un diseño que nos permita crear un entorno en el que un código almacenado remotamente se ejecuta localmente al cliente, sin requerir que éste disponga de dicho código (_kernel_ local y cuadernillo remoto). En el caso concreto del ejercicio que hemos diseñado para hacer las primeras pruebas, conseguiremos que este código remoto tenga acceso a la cámara local del cliente y se pueda resolver el ejercicio a través de ella. 

Este diseño pasa, en primera instancia, por el estudio de Jupyter y sus Cuadernillos y, en segunda, por el estudio de la Web y los mecanismos de transmisión de datos multimedia.

Estas primeras semanas estarán se acercarán más a un proceso de pura investigación que poco a poco irá dando paso a un proceso mixto de pruebas, análisis e investigación para finalmente acabar con la selección de las herramientas y mecanismos que nos permitan comenzar la implementación en búsqueda de la solución.

## Semana 2

Una vez que el nodo del ejercicio ha sido modificado para aceptar una fuente de vídeo local, hemos tratado de utilizarlo desde un Cuadernillo. Además de esta modalidad, han funcionado también el resto de posibles fuente de vídeo (recurso estático almacenado en el sistema de ficheros, _streaming_ web, _plugins_ ROS o ICE).

##### [YOUTUBE VIDEO] Selectable Source (Camera Stream).
[![Selectable Source](https://img.youtube.com/vi/meVvdFs3Vt0/0.jpg)](https://www.youtube.com/watch?v=meVvdFs3Vt0 "")
##### [YOUTUBE VIDEO] Selectable Source (Output).
[![Output](https://img.youtube.com/vi/D8dOrv6z3BM/0.jpg)](https://www.youtube.com/watch?v=D8dOrv6z3BM "")

## Semana 1

El primer paso para el proyecto de ejecución mixta de ejercicios de visión artificial pasa por crear un ejercicio de prueba. Hemos escogido Jupyter como primera aproximación al entorno de construcción de los ejercicios, pues se accede a él a través de la web (que nos acerca al objetivo de ser multiplataforma y accesibles), y porque se basa en código Python, un lenguaje muy sencillo de utilizar a la par que potente.

Un primer paso para este ejercicio de visión artificial, que será un simple Filtro de Color, será acceder a la cámara del usuario (típicamente webcam integrada) para extraer de ella las imágenes que se usarán para el ejercicio, sobre las que se aplicará el procesamiento de imagen.

Incluímos en este primer paso un fichero de configuración para que el _back-end_ sea capaz de reconocer las interfaces de la cámara en el sistema del usuario. En el futuro habrá que solucionar el acceso de modo remoto.

Plantemos también una primera versión de la solución para ser utilizada de aquí en adelnte como test para el proceso de implementación del resto del mecanismo de ejecución compartida. 

![Input](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/inputImage.png)
![Smooth](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/smoothImage.png)
![HSV](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/hsvImage.png)
![Threshold](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/thresholdImage.png)
![Output](https://github.com/cawadall/TFM-Carlos-Awadallah/docs/img/filteredImage.png)

También hemos añadido un botón para la visualización de las imágenes en el propio cuadernillo, con fines depurativos. Iremos refniando este mecanismo para tratar de conseguir un flujo de vídeo.

##### [YOUTUBE VIDEO] Button to print Video (Camera Stream).
[![Print Video Button](https://img.youtube.com/vi/ouDR7TC1_uI/0.jpg)](https://www.youtube.com/watch?v=ouDR7TC1_uI "")
##### [YOUTUBE VIDEO] Button to print Video (Filtered Images).
[![Print Video Button](https://img.youtube.com/vi/Qq9KgkcM5FU/0.jpg)](https://www.youtube.com/watch?v=Qq9KgkcM5FU "")

