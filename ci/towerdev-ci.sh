#!/bin/bash

# towerdev-ci - Test Suite

# towerdev-ci Options & Global Defaults

operation=$1
supportedVersions=( "3.6.0" "3.6.1" "3.6.2" "3.6.3" "3.6.4" "3.6.5" "3.6.6" "3.7.0" "3.7.1" "3.7.2" "3.7.3" "3.8.0" )
supportedChannels=( "3.6.0" "3.7.0" "3.8.0" )
specialContainers=( "ssh" )

# towerdev-ci Functions

usage() {
    echo "towerdev-ci: CI for towerdev"
    echo "Usage:"
    echo "    --help: Show usage"
    echo "    --build-all: Build all supported versions of Ansible Tower"
    echo "    --build-channel: Build all supported versions of Ansible Tower by channel"
    echo "    --run-all: Create containers for all supported versions of Ansible Tower"
    echo "    --run-channel: Create containers for release channel of Ansible Tower"
    echo "    --run-cluster: Create container cluster for supported channels of Ansible Tower"
    echo "    --test-images: Test --images command"
    echo "    --run-all-tests: Run all towerdev tests"
}

buildAll() {
    echo -e "\e[33mINFO: Running build for all supported releases of Ansible Tower...\e[0m"
    echo -e "\e[31mWARNING: Pausing for 15 seconds! About to remove all Tower containers! CTRL+C if you want to stop this!\e[0m"
    sleep 15s
    # Removal of all Tower containers
    towerContainers=( $(docker ps -a | grep ansibletower | awk '{ print $1 }') )

    for i in "${towerContainers[@]}"; do
        docker rm -f "$i";
    done

    # Removing all Tower images
    echo -e "\e[33mINFO: Clearing all pre-existing images...\e[0m"
    existingImages=( $(towerdev-cli --images) )

    for i in "${existingImages[@]}"; do 
        docker rmi "$i";
    done

    for i in "${supportedVersions[@]}"; do
        time towerdev-cli --build "$i";
        buildStatus=$?
        if [ "$buildStatus" = 0 ]; then
            echo -e "\e[32mINFO: BUILD PASSED for $i"
        else
            echo -e "\e[31mERROR: BUILD FAILED for $i"
            exit 1
        fi
    done
}

buildChannel() {
    channel=$2
    if [[ "$channel" = *3.6* ]]; then
        echo -e "\e[33mINFO: Running builds for all releases in the 3.6.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.6.[0-9]); do
            time towerdev-cli --build "$i";
            buildStatus=$?
            if [ "$buildStatus" = 0 ]; then
                echo -e "\e[32mINFO: BUILD PASSED for $i"
            else
                echo -e "\e[31mERROR: BUILD FAILED for $i"
                exit 1
            fi
        done

    elif [[ "$channel" = *3.7* ]]; then
        echo -e "\e[33mINFO: Running builds for all releases in the 3.7.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.7.[0-9]); do
            time towerdev-cli --build "$i";
            buildStatus=$?
            if [ "$buildStatus" = 0 ]; then
                echo -e "\e[32mINFO: BUILD PASSED for $i"
            else
                echo -e "\e[31mERROR: BUILD FAILED for $i"
                exit 1
            fi
        done

    elif [[ "$channel" = *3.8* ]]; then
        echo -e "\e[33mINFO: Running builds for all releases in the 3.8.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.8.[0-9]); do
            time towerdev-cli --build "$i";
            buildStatus=$?
            if [ "$buildStatus" = 0 ]; then
                echo -e "\e[32mINFO: BUILD PASSED for $i"
            else
                echo -e "\e[31mERROR: BUILD FAILED for $i"
                exit 1
            fi
        done

    else
        echo -e "\e[31mERROR: Please specify a valid Tower release channel.\e[0m"
        exit 1
    fi
}

runAll() {
    echo -e "\e[33mINFO: Creating containers for all supported releases of Ansible Tower...\e[0m"

    for i in "${towerContainers[@]}"; do
        docker rm -f "$i";
    done

    for i in "${supportedVersions[@]}"; do
        time towerdev-cli --run "$i" "" centos7 tower-"$i";
        runStatus=$?
        if [ "$runStatus" = 0 ]; then
            echo -e "\e[32mINFO: Creation of $i container was successful!"
        else
            echo -e "\e[31mERROR: Creation of $i container failed!"
            exit 1
        fi
    done
}

runChannel() {
    channel=$2
    if [[ "$channel" = *3.6* ]]; then
        echo -e "\e[33mINFO: Creating containers for all releases in the 3.6.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.6.[0-9]); do
            time towerdev-cli --run "$i" "" centos7 tower-"$i";
            runStatus=$?
            if [ "$runStatus" = 0 ]; then
                echo -e "\e[32mINFO: Creation of $i container was successful!"
            else
                echo -e "\e[31mERROR: Creation of $i container failed!"
                exit 1
            fi
        done

    elif [[ "$channel" = *3.7* ]]; then
        echo -e "\e[33mINFO: Creating containers for all releases in the 3.7.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.7.[0-9]); do
            time towerdev-cli --run "$i" "" centos7 tower-"$i";
            runStatus = $?
            if [ "$runStatus" = 0 ]; then
                echo -e "\e[32mINFO: Creation of $i container was successful!"
            else
                echo -e "\e[31mERROR: Creation of $i container failed!"
                exit 1
            fi
        done

    elif [[ "$channel" = *3.8* ]]; then
        echo -e "\e[33mINFO: Creating containers for all releases in the 3.8.x release channel...\e[0m"

        for i in $(echo "${supportedVersions[@]}" | grep -o 3.8.[0-9]); do
            time towerdev-cli --run "$i" "" centos7 tower-"$i";
            runStatus=$?
            if [ "$runStatus" = 0 ]; then
                echo -e "\e[32mINFO: Creation of $i container was successful!"
            else
                echo -e "\e[31mERROR: Creation of $i container failed!"
                exit 1
            fi
        done

    else
        echo -e "\e[31mERROR: Please specify a valid Tower release channel.\e[0m"
        exit 1
    fi
}

runSpecial() {
    echo -e "\e[33mINFO: Creating special containers...\e[0m"

    for i in "${specialContainers[@]}"; do
        time towerdev-cli --special "$i" "" centos7 "$i"-ci-test;
        runStatus=$?
        if [ "$runStatus" = 0 ]; then
            echo -e "\e[32mINFO: Creation of $i container was successful!"
            towerdev-cli --delete "$i"-ci-test
        else
            echo -e "\e[31mERROR: Creation of $i container failed!"
            exit 1
        fi
    done
}

runCluster() {
    echo -e "\e[33mINFO: Creating container clusters for all supported channels of Ansible Tower...\e[0m"

    for i in "${supportedChannels[@]}"; do
        time towerdev-cli --cluster "$i" centos7 "$i"-ci;
        clusterStatus=$?
        if [ "$clusterStatus" = 0 ]; then
            echo -e "\e[32mINFO: Creation of $i container cluster was successful!"
            towerdev-cli --delete "$i"-ci-0
            towerdev-cli --delete "$i"-ci-1
            towerdev-cli --delete "$i"-ci-2
        else
            echo -e "\e[31mERROR: Creation of $i container cluster failed."
            towerdev-cli --delete "$i"-ci-0
            towerdev-cli --delete "$i"-ci-1
            towerdev-cli --delete "$i"-ci-2
            exit 1
        fi
    done
}

testImages() {
    echo -e "\e[33mINFO: Testing --images...\e[0m"
    time towerdev-cli --images
    imagesStatus=$?

    if [ "$imagesStatus" = 0 ]; then
        echo -e "\e[32mINFO: Test for --images passed!"
    else
        echo -e "\e[31mERROR: Test for --images failed!"
        exit 1
    fi
}

testDelete() {
    echo -e "\e[33mINFO: Testing --delete...\e[0m"
    towerdev-cli --special ssh "" centos7 ci-delete-test
    time towerdev-cli --delete ci-delete-test
    deleteStatus=$?

    if [ "$deleteStatus" = 0 ]; then
        echo -e "\e[32mINFO: Test for --delete passed!"
    else
        echo -e "\e[31mERROR: Test for --delete failed!"
        exit 1
    fi
}

if [ "$operation" = "--help" ]; then
    usage
elif [ "$operation" = "--build-all" ]; then
    buildAll
elif [ "$operation" = "--build-channel" ]; then
    channel=$2
    buildChannel
elif [ "$operation" = "--run-all" ]; then
    runAll
elif [ "$operation" = "--run-channel" ]; then
    channel=$2
    runChannel
elif [ "$operation" = "--run-special" ]; then
    runSpecial
elif [ "$operation" = "--run-cluster" ]; then
    runCluster
elif [ "$operation" = "--test-images" ]; then
    testImages
elif [ "$operation" = "--run-all-tests" ]; then
    buildAll
    runAll
    runSpecial
    runCluster
    testImages
    testDelete
else
    usage
    echo -e "\e[31mERROR: Please specify a valid option for towerdev-ci.\e[0m"
    exit 1
fi
