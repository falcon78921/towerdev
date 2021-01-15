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

import os
import towerdev.common
from colors import *
from configparser import ConfigParser

# Invoke dockerClient()

dockerClient = towerdev.common.dockerClient()

def buildImage(towerVersion, debug=False, stream=True):
    """Builds Tower container image using supplied arguments"""

    buildArgs=dict(towerVersion=towerVersion, debug=debug)

    if debug == True:
        print(color("INFO: Building Ansible Tower container image...", fg="yellow"))
        print(buildArgs)

    buildDict = dict(TOWER_VERSION=towerVersion)

    # Prevents oddities when building nightlies; not so great for security
    gpgCmd = "sed -i 's/gpgcheck=1/gpgcheck=0/g' /opt/ansible-tower-setup-{0}-1/roles/repos_el/templates/tower_bundle.j2".format(towerVersion)
    setupCmd = '/bin/bash -c "cd /opt/ansible-tower-setup-{0}-1 && ./setup.sh"'.format(towerVersion)

    # Check for Dockerfile & os file
    dockerFileExists = os.path.isfile("Dockerfile")
    osFileExists = os.path.isfile("os")

    # If a Dockerfile isn't detected, we need to address this
    if dockerFileExists and osFileExists == True:
        # Read in build information
        osConfig = ConfigParser()
        osConfig.read("os")
        centosVersion = osConfig.get('buildConfig', 'os')
        # Build Tower image based on relative Dockerfile
        buildImage = dockerClient.images.build(path="./", buildargs=buildDict, quiet=False, tag="ansibletower{0}_build".format(towerVersion), forcerm=True)
        # Initiate a container instance based off of first level image; bind necessary host components for systemd
        towerContainer = dockerClient.containers.run('ansibletower{0}_build'.format(towerVersion), privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name="build-{0}".format(towerVersion))
        # Run necessary prep commands and call ./setup.sh
        runGpgCmd = towerContainer.exec_run(cmd=gpgCmd)

        # Stream output based on option
        if stream:
            lowLevelClient = towerdev.common.apiClient()
            createExec = lowLevelClient.exec_create(container="build-{0}".format(towerVersion), cmd=setupCmd)
            runSetupCmd = lowLevelClient.exec_start(exec_id=createExec['Id'], stream=True, detach=False)

            for line in runSetupCmd:
                print(line.decode('utf-8'))

            inspect = lowLevelClient.exec_inspect(exec_id=createExec['Id'])
            setupCmdCode = inspect['ExitCode']

        else:
            runSetupCmd = towerContainer.exec_run(cmd=setupCmd)

        # If image build is successful, commit to a new image
        if runGpgCmd[0] == 0 and setupCmdCode == 0:
            print(color("INFO: Committing Tower container to image...", fg="yellow"))
            containerCommit = towerContainer.commit(repository="ansibletower/{0}".format(centosVersion), tag=towerVersion)
            print(color("INFO: Removing build container...", fg="yellow"))
            deleteBuildContainer = towerContainer.remove(force=True)
            print(color("INFO: Removing build image...", fg="yellow"))
            deleteBuildImage = dockerClient.images.remove(image="ansibletower{0}_build".format(towerVersion))
            buildStatus = True
        else:
            print(color("INFO: Removing build container...", fg="yellow"))
            deleteBuildContainer = towerContainer.remove(force=True)
            print(color("INFO: Removing build image...", fg="yellow"))
            deleteBuildImage = dockerClient.images.remove(image="ansibletower{0}_build".format(towerVersion))
            print(color("ERROR: Docker container build failed. Please check build output and retry.", fg="red"))
            buildStatus = False

    else:
        print(color("ERROR: No Dockerfile or os file detected. Please make sure to launch towerdev from a Docker build directory with a Dockerfile and os file.", fg="red"))

    return buildStatus
