#!/usr/bin/env python3

''' towerdev - Ansible Tower Testing Framework

MIT License

Copyright © 2021 falcon78921

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import re
import sys
import towerdev.common
from colors import *

# Invoke dockerClient()

dockerClient = towerdev.common.dockerClient()

def imageCheck(towerVersion):
    """Check to see if Tower image has been built for specified version"""
    status = None
    dockerImages = str(dockerClient.images.list())
    towerImages = str(re.findall(r'ansibletower/centos\w:\w.\w.\w', dockerImages))
    builtVersions = re.findall(r'[2-3].[0-9].[0-9]', towerImages)

    # Loop through all Tower images and see if one matches
    for i in builtVersions:
        if towerVersion == i:
            print(color("INFO: Yay! We have {0} in stock!".format(towerVersion), fg="yellow"))
            break
            status = True
        elif towerVersion != i:
            print(color("INFO: {0} does not match {1}. Let's keep trying...".format(i, towerVersion), fg="yellow"))

    return status

def deleteContainer(containerName):
    """Delete specified container"""
    """True means that deletion was successful."""
    """False means that deletion was unsuccessful."""
    deleteContainer = dockerClient.containers.get(container_id=containerName)
    deleteContainer.stop()
    deleteContainer.remove()

    containersList = dockerClient.containers.list(filters={'name': containerName})

    if len(containersList) == 0:
        deletionStatus = True
    else:
        deletionStatus = False

    return deletionStatus

def listImages():
    """List all Tower images using docker-py"""
    dockerImages = str(dockerClient.images.list())
    towerImages = re.findall(r'ansibletower/centos\w:\w.\w.\w', dockerImages)

    return towerImages
