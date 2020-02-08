import os, django
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tfm_webserver.settings")
channel_layer = get_channel_layer()
