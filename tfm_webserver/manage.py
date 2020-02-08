#!/usr/bin/env python
import os
import sys, commands
import docker
from django.conf import settings

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tfm_webserver.settings")

    docker_client = docker.DockerClient()
    containers = docker_client.containers.list(all=True, filters={"name": r"([*-z]+)\-([A-z]+)+\-+([0-9]+\.+[0-9]+)", "ancestor": settings.DOCKER_SIMULATION_IMAGE})
    [container.kill() for container in containers]

    execute_from_command_line(sys.argv)
