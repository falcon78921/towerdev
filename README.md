<h1>towerdev: Ansible Tower Testing Framework</h1>

<h2>Purpose:</h2>

Built on Docker, Ansible Tower containers are created with certain customizations.
The use of containers allows for speedy deployments of Ansible Tower and version control.

This repository tracks two components: `towerdev` and `towerdev-cli`. `towerdev`
is the Python library that is built around `docker-py` and acts as the core engine. 
`towerdev-cli` is the command line tool that wraps around `towerdev`. With the 
help of `pyinstaller`, `towerdev-cli` can be built into a standalone binary.

`towerdev-cli` is intended for testing & demo. The entire installation of 
Ansible Tower is baked into a single container image. Tower clusters are
dependent on external databases, which can either be on a dedicated PostgreSQL
instance or in another container. If you want to run Tower with separated services
(e.g. container pods), I would recommend deploying Tower with
[OKD](https://www.okd.io/) or `docker-compose`.

<h2>towerdev-cli Usage:</h2>

~~~
usage: towerdev-cli [-h] [--build <TOWER_VERSION>]
                    [--run <TOWER_VERSION> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>]
                    [--special <PURPOSE> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>]
                    [--cluster <TOWER_VERSION> <OS_VERSION> <NAMING_CONVENTION>]
                    [--delete <CONTAINER_NAME>] [--login <CONTAINER_NAME>]
                    [--images]

towerdev-cli: Ansible Tower Testing Framework

optional arguments:
  -h, --help            show this help message and exit
  --build <TOWER_VERSION>
                        Build a single Ansible Tower image
  --run <TOWER_VERSION> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>
                        Deploy a single Ansible Tower container from a pre-
                        existing image
  --special <PURPOSE> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>
                        Deploy a specialized container
  --cluster <TOWER_VERSION> <OS_VERSION> <NAMING_CONVENTION>
                        Build & deploy an Ansible Tower container cluster
  --delete <CONTAINER_NAME>
                        Stop and remove an Ansible Tower container
  --login <CONTAINER_NAME>
                        Log into an Ansible Tower container
  --images              List all available Ansible Tower images
~~~

<h2>Examples:</h2>

Build container image for specific version of Ansible Tower:

~~~
towerdev-cli --build <TOWER_VERSION>
towerdev-cli --build 3.7.0
~~~

Run a container of Ansible Tower:

~~~
towerdev-cli --run <TOWER_VERSION> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>
towerdev-cli --run 3.7.3 1050 centos7 tower-3.7.3
~~~

If you want Docker to decide the external port, please pass empty double quotes (`""`):

~~~
towerdev-cli --run <TOWER_VERSION> <EXTERNAL_PORT> <OS_VERSION> <CONTAINER_NAME>
towerdev-cli --run 3.7.3 "" centos7 tower-3.7.3
~~~

Build a container cluster using a certain version of Ansible Tower:

~~~
towerdev-cli --cluster <TOWER_VERSION> <OS_VERSION> <NAMING_CONVENTION>
towerdev-cli --cluster 3.7.3 centos7 test
~~~

<h2>Getting Started</h2>

<h3>Building Base Images:</h3>

Before attempting to build Tower images with `towerdev-cli`, please make sure to
build the images in `build/supplementals`. There are two images that act as the base
of the Tower installation. `towerdev` uses the official CentOS images and modifies them
for `systemd`.

You can build the images in `build/supplementals` using the following commands:

~~~
docker build -t centos7/systemd .
docker build -t centos8/systemd .
~~~

Please make sure to run the preceding commands in their respective build directories. For more information on the base images, please reference the `README.md` file in the corresponding image directory.

<h3>Building Tower Images:</h3>

Once you have built the base images, you can now use `towerdev-cli` to build the Tower images. In order to build a Tower image, please run `towerdev-cli --build <TOWER_VERSION>` in the appropriate build directory.

If you want to build with CentOS 7, please run `towerdev-cli --build <TOWER_VERSION>` in the `build/ansibletower/centos7` directory. If you want to build with CentOS 8, please run `towerdev-cli --build <TOWER_VERSION>` in the `build/ansibletower/centos8` directory.

<h2>Notes:</h2>

* Although `towerdev-cli` is open-source, Ansible Tower requires a valid Red Hat Ansible Automation Platform entitlement. Please contact [Red Hat](https://www.ansible.com/products/tower) for more information on purchasing a license/entitlement. You can also
deploy `awx` if you do not want to purchase Tower, however, `towerdev-cli` is not built for deploying `awx`. Please reference [ansible/awx](https://github.com/ansible/awx) for more information on deployment.

* When running a 3.6.x cluster with `towerdev-cli --cluster`, the deployment may fail if Tower has not been activated beforehand. In order to remedy, you can run `towerdev-cli --cluster <TOWER_VERSION>` (i.e. `<TOWER_VERSION>` is the desired 3.6.x version) and then activate by navigating to one of the instances. Once you have activated Tower using a valid license or Red Hat login, you can rerun `./setup.sh` by executing the following command with `docker exec`:

   ~~~
   docker exec -it test-2 /bin/bash -c "cd /opt/ansible-tower-setup-3.6.0-1 && ./setup.sh"
   ~~~

* `towerdev-cli --cluster` will always choose the last container in the series for executing `./setup.sh`. For example, if you create a 3.6.4 cluster of three containers and have the naming convention be `test`, then `test-2` will have the modified `inventory` file and `towerdev-cli` will execute from there.
