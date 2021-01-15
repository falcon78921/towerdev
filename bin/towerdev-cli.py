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

import argparse
import os
import sys
from colors import *
from towerdev import build
from towerdev import run
from towerdev import utilities

# Global options & usage

parser = argparse.ArgumentParser(description="towerdev-cli: Ansible Tower Testing Framework")
parser.add_argument('--build', help='Build a single Ansible Tower image', metavar="<TOWER_VERSION>", type=str, nargs=1)
parser.add_argument('--run', help='Deploy a single Ansible Tower container from a pre-existing image', metavar=("<TOWER_VERSION>", "<EXTERNAL_PORT>", "<OS_VERSION>", "<CONTAINER_NAME>"), type=str, nargs=4)
parser.add_argument('--special', help='Deploy a specialized container', metavar=("<PURPOSE>", "<EXTERNAL_PORT>", "<OS_VERSION>", "<CONTAINER_NAME>"), type=str, nargs=4)
parser.add_argument('--cluster', help='Build & deploy an Ansible Tower container cluster', metavar=("<TOWER_VERSION>", "<OS_VERSION>", "<NAMING_CONVENTION>"), type=str, nargs=3)
parser.add_argument('--delete', help='Stop and remove an Ansible Tower container', metavar=("<CONTAINER_NAME>"), type=str, nargs=1)
parser.add_argument('--login', help='Log into an Ansible Tower container', metavar=("<CONTAINER_NAME>"), type=str, nargs=1)
parser.add_argument('--images', help='List all available Ansible Tower images', action='store_true')

args = parser.parse_args()

if args.build:
    towerVersion = sys.argv[2]
    print(color("INFO: Starting Ansible Tower container build...", fg="yellow"))
    buildStatus = build.buildImage(towerVersion=towerVersion)

    if buildStatus:
        print(color("INFO: Container image for {0} was successfully built!".format(towerVersion), fg="yellow"))
        sys.exit(0)
    else:
        print(color("ERROR: Container image for {0} was not successfully built.".format(towerVersion), fg="red"))
        sys.exit(1)

elif args.run:
    towerVersion = sys.argv[2]
    externalPort = sys.argv[3]
    osVersion = sys.argv[4]
    containerName = sys.argv[5]

    if not externalPort:
        externalPort = None

    if len(towerVersion) <= 0:
        print(color("ERROR: Please provide a version of Tower that you wish to build", fg="red"))
        sys.exit(1)
    elif len(osVersion) <= 0:
        print(color("ERROR: Please provide an operating system version", fg="red"))
        sys.exit(1)
    elif len(containerName) <= 0:
        print(color("ERROR: Please provide a name for the Tower container", fg="red"))
        sys.exit(1)
    else:
        print(color("INFO: Starting Ansible Tower container from pre-existing image...", fg="yellow"))
        runContainerStatus = run.runTowerContainer(towerVersion=towerVersion, externalPort=externalPort, osVersion=osVersion, containerName=containerName)

    if runContainerStatus:
        print(color("INFO: {0} was successfully created!".format(containerName), fg="yellow"))
        sys.exit(0)
    else:
        print(color("ERROR: Creation of {0} failed.".format(containerName), fg="red"))
        sys.exit(1)

elif args.special:
    purpose = sys.argv[2]
    externalPort = sys.argv[3]
    osVersion = sys.argv[4]
    containerName = sys.argv[5]

    if not externalPort:
        externalPort = None

    if len(purpose) <= 0:
        print(color("ERROR: Please provide a specialized purpose for the container", fg="red"))
        sys.exit(1)
    elif len(osVersion) <= 0:
        print(color("ERROR: Please provide an operating system version", fg="red"))
        sys.exit(1)
    elif len(containerName) <= 0:
        print(color("ERROR: Please provide a name for the Tower container", fg="red"))
        sys.exit(1)
    else:
        print(color("INFO: Starting specialized container of type: {0}".format(purpose), fg="yellow"))
        runSpecialStatus = run.runContainer(purpose=purpose, externalPort=externalPort, osVersion=osVersion, containerName=containerName)

    if runSpecialStatus:
        print(color("INFO: {0} was successfully created!".format(containerName), fg="yellow"))
        sys.exit(0)
    else:
        print(color("ERROR: Creation of {0} failed.".format(containerName), fg="red"))
        sys.exit(1)

elif args.cluster:
    towerVersion = sys.argv[2]
    osVersion = sys.argv[3]
    namingConvention = sys.argv[4]

    if len(towerVersion) <= 0:
        print(color("ERROR: Please provide a version of Tower that you wish to build", fg="red"))
        sys.exit(1)
    elif len(osVersion) <= 0:
        print(color("ERROR: Please provide an operating system version", fg="red"))
        sys.exit(1)
    elif len(namingConvention) <= 0:
        print(color("ERROR: Please provide a name for the Tower container", fg="red"))
        sys.exit(1)
    else:
        print(color("INFO: Starting Tower container cluster...", fg="yellow"))
        clusterStatus = run.runContainerCluster(towerVersion=towerVersion, osVersion=osVersion, namingConvention=namingConvention)

    if clusterStatus:
        print(color("INFO: {0} cluster was successfully created!".format(towerVersion), fg="yellow"))
        sys.exit(0)
    else:
        print(color("ERROR: Creation of {0} cluster failed.".format(towerVersion), fg="red"))
        sys.exit(1)

elif args.login:
    containerName = sys.argv[2]

    # Open /bin/bash session from operating system using os.system() call
    dockerLoginCmd = "docker exec -it {0} /bin/bash".format(containerName)
    os.system(dockerLoginCmd)

elif args.delete:
    containerName = sys.argv[2]
    deletionStatus = utilities.deleteContainer(containerName=containerName)

    if deletionStatus:
        print(color("INFO: {0} was successfully deleted!".format(containerName), fg="yellow"))
        sys.exit(0)
    else:
        print(color("ERROR: {0} was not successfully deleted. Does {0} exist?".format(containerName), fg="red"))
        sys.exit(1)

elif args.images:
    listImages = utilities.listImages()

    if len(listImages) > 0:
        for i in listImages:
            print(i)
        sys.exit(0)
    else:
        print(color("ERROR: No Tower images were found. Please try building one using --build.", fg="red"))
        sys.exit(1)

else:
    print(color("ERROR: Please specify a valid operation and its corresponding options", fg="red"))
    sys.exit(1)
