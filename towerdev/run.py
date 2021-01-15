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

import towerdev.common
import towerdev.utilities
from colors import *

# Invoke dockerClient()

dockerClient = towerdev.common.dockerClient()

def runContainer(purpose, externalPort, osVersion, containerName, debug=True, **kwargs):
    """Run supplemental container from pre-existing image"""

    # Optional debug that prints a dict of options
    if debug == True:
        runSpecialOpts = dict(purpose=purpose, externalPort=externalPort, osVersion=osVersion, containerName=containerName)
        print(runSpecialOpts)

    # Determines what we do based on purpose
    if purpose == "ssh":
        if osVersion == "centos7":
            sshContainer = dockerClient.containers.run('centos7/systemd', privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name=containerName, ports={'22/tcp':externalPort})
        elif osVersion == "centos8":
            sshContainer = dockerClient.containers.run('centos8/systemd', privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''},  detach=True, name=containerName, ports={'22/tcp':externalPort})

    containersList = dockerClient.containers.list(filters={'name': containerName})

    if len(containersList) == 1:
        creationStatus = True
    else:
        creationStatus = False

    return creationStatus

def runContainerCluster(towerVersion, osVersion, namingConvention, stream=True, **kwargs):
    """Run Tower containers in a clustered setup"""
    # runContainerCluster() defaults; can be overriden via **kwargs
    externalPort = None
    containerCount = 3
    debug = True
    loadBalance = False

    # Optional debug that prints a dict of options
    if debug:
        runClusterOpts = dict(towerVersion=towerVersion, osVersion=osVersion, loadBalance=loadBalance, namingConvention=namingConvention, externalPort=externalPort, containerCount=containerCount, debug=debug)
        print(runClusterOpts)

    # Check to see if specified towerVersion has image built
    check = towerdev.utilities.imageCheck(towerVersion)

    # How we proceed with imageCheck() return
    if check is False:
        print(color("ERROR: Deployment of container cluster failed. Please make sure the specified version of Tower has an image built.", fg="red"))
        return False
    else:
        for c in range(containerCount):
            runTowerContainer(towerVersion=towerVersion, externalPort=externalPort, osVersion=osVersion, containerName="{0}-{1}".format(namingConvention,c))

    clusterContainers = dockerClient.containers.list(filters={'name': '{0}-*'.format(namingConvention)})
    containerIps = []

    # Gather container IPs for inventory fillout
    for c in range(len(clusterContainers)):
        containerIp = clusterContainers[c].attrs['NetworkSettings']['IPAddress']
        containerIps.append(containerIp)

    print(clusterContainers[0])

    # Choose inventory file based on towerVersion
    if "3.5" in towerVersion:
        chooseInventoryCmd = 'mv /opt/ansible-tower-setup-{0}-1/cluster_inventory_3.5.x /opt/ansible-tower-setup-{0}-1/inventory'.format(towerVersion)
        runInventoryCmd = clusterContainers[0].exec_run(cmd=chooseInventoryCmd)
    elif "3.6" in towerVersion:
        chooseInventoryCmd = 'mv /opt/ansible-tower-setup-{0}-1/cluster_inventory_3.6.x /opt/ansible-tower-setup-{0}-1/inventory'.format(towerVersion)
        runInventoryCmd = clusterContainers[0].exec_run(cmd=chooseInventoryCmd)
    elif "3.7" in towerVersion:
        chooseInventoryCmd = 'mv /opt/ansible-tower-setup-{0}-1/cluster_inventory_3.7.x /opt/ansible-tower-setup-{0}-1/inventory'.format(towerVersion)
        runInventoryCmd = clusterContainers[0].exec_run(cmd=chooseInventoryCmd)
    elif "3.8" in towerVersion:
        chooseInventoryCmd = 'mv /opt/ansible-tower-setup-{0}-1/cluster_inventory_3.8.x /opt/ansible-tower-setup-{0}-1/inventory'.format(towerVersion)
        runInventoryCmd = clusterContainers[0].exec_run(cmd=chooseInventoryCmd)

    # Choose messaging backend based on towerVersion
    if "3.5" in towerVersion:
        for i in containerIps:
            modifyInventoryCmd = 'sed -i "2i{0} rabbitmq_host={0}" /opt/ansible-tower-setup-{1}-1/inventory'.format(i, towerVersion)
            runInventoryCmd = clusterContainers[0].exec_run(cmd=modifyInventoryCmd)
    elif "3.6" in towerVersion:
        for i in containerIps:
            modifyInventoryCmd = 'sed -i "2i{0} rabbitmq_host={0}" /opt/ansible-tower-setup-{1}-1/inventory'.format(i, towerVersion)
            runInventoryCmd = clusterContainers[0].exec_run(cmd=modifyInventoryCmd)
    elif "3.7" in towerVersion:
        for i in containerIps:
            modifyInventoryCmd = 'sed -i "2i{0} routable_hostname={0}" /opt/ansible-tower-setup-{1}-1/inventory'.format(i, towerVersion)
            runInventoryCmd = clusterContainers[0].exec_run(cmd=modifyInventoryCmd)
    elif "3.8" in towerVersion:
        for i in containerIps:
            modifyInventoryCmd = 'sed -i "2i{0} routable_hostname={0}" /opt/ansible-tower-setup-{1}-1/inventory'.format(i, towerVersion)
            runInventoryCmd = clusterContainers[0].exec_run(cmd=modifyInventoryCmd)

    # Call ./setup.sh from first container in list
    setupCmd = '/bin/bash -c "cd /opt/ansible-tower-setup-{0}-1 && ./setup.sh"'.format(towerVersion)
    setupLbCmd = '/bin/bash -c "cd /opt/ansible-tower-setup-{0}-1 && ./setup.sh -e nginx_disable_https=true"'.format(towerVersion)
    inventoryDbVersion = towerVersion.replace(".", "")
    modifyInventoryDbCmd = "sed -i 's/XXX/{0}/g' /opt/ansible-tower-setup-{1}-1/inventory".format(inventoryDbVersion, towerVersion)
    runDatabaseCmd = clusterContainers[0].exec_run(cmd=modifyInventoryDbCmd)

    if loadBalance:
        print(color("INFO: Running ./setup.sh with load balance configuration...", fg="yellow"))

        # Stream output based on option
        if stream:
            lowLevelClient = towerdev.common.apiClient()
            calcRunContainer = len(clusterContainers) - 1
            createExec = lowLevelClient.exec_create(container="{0}-{1}".format(namingConvention, calcRunContainer), cmd=setupLbCmd)
            runSetupCmd = lowLevelClient.exec_start(exec_id=createExec['Id'], stream=True, detach=False)

            for line in runSetupCmd:
                print(line.decode('utf-8'))

            inspect = lowLevelClient.exec_inspect(exec_id=createExec['Id'])
            setupCmdCode = inspect['ExitCode']

            containersList = dockerClient.containers.list(filters={'name': '{0}-*'.format(namingConvention)})

            if len(containersList) == containerCount:
                clusterStatus = True
            else:
                clusterStatus = False

            if setupCmdCode is not 0:
                clusterStatus = False

        else:
            runSetupCmd = towerContainer.exec_run(cmd=setupLbCmd)

    else:
        print(color("INFO: Running ./setup.sh with no load balance configuration...", fg="yellow"))

        # Stream output based on option
        if stream:
            lowLevelClient = towerdev.common.apiClient()
            calcRunContainer = len(clusterContainers) - 1
            createExec = lowLevelClient.exec_create(container="{0}-{1}".format(namingConvention, calcRunContainer), cmd=setupCmd)
            runSetupCmd = lowLevelClient.exec_start(exec_id=createExec['Id'], stream=True, detach=False)

            for line in runSetupCmd:
                print(line.decode('utf-8'))

            inspect = lowLevelClient.exec_inspect(exec_id=createExec['Id'])
            setupCmdCode = inspect['ExitCode']
            containersList = dockerClient.containers.list(filters={'name': '{0}-*'.format(namingConvention)})

            if len(containersList) == containerCount:
                clusterStatus = True
            else:
                clusterStatus = False

            if setupCmdCode is not 0:
                clusterStatus = False

        else:
            runSetupCmd = towerContainer.exec_run(cmd=setupCmd)
            containersList = dockerClient.containers.list(filters={'name': '{0}-*'.format(namingConvention)})

            if len(containersList) == containerCount:
                clusterStatus = True
            else:
                clusterStatus = False

            if runSetupCmd[0] is not 0:
                clusterStatus = False

    return clusterStatus


def runTowerContainer(towerVersion, externalPort, osVersion, containerName, debug=False, **kwargs):
    """Runs Tower container from pre-existing image"""
    allowedMemory = None

    # Optional debug that prints a dict of options
    if debug == True:
        runOpts = dict(towerVersion=towerVersion, externalPort=externalPort, osVersion=osVersion, containerName=containerName)
        print(runOpts)

    # Determines what we do based on externalPort input
    if not externalPort:
        if allowedMemory is not None:
            towerContainer = dockerClient.containers.run('ansibletower/{0}:{1}'.format(osVersion, towerVersion), privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name=containerName, mem_limit=allowedMemory, ports={'443/tcp':None})
        else:
            towerContainer = dockerClient.containers.run('ansibletower/{0}:{1}'.format(osVersion, towerVersion), privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name=containerName, ports={'443/tcp':None})
    else:
        if allowedMemory is not None:
            towerContainer = dockerClient.containers.run('ansibletower/{0}:{1}'.format(osVersion, towerVersion), privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name=containerName, mem_limit=allowedMemory, ports={'443/tcp':externalPort})
        else:
            towerContainer = dockerClient.containers.run('ansibletower/{0}:{1}'.format(osVersion, towerVersion), privileged=False, volumes={'/sys/fs/cgroup': {'bind':'/sys/fs/cgroup', 'mode':'ro'}}, tmpfs={'/tmp':'exec', '/run':''}, detach=True, name=containerName, ports={'443/tcp':externalPort})

    containersList = dockerClient.containers.list(filters={'name': containerName})

    if len(containersList) == 1:
        creationStatus = True
    else:
        creationStatus = False

    return creationStatus

