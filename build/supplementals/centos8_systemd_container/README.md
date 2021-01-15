<h1>CentOS 8 systemd Container</h1>

<h2>Purpose:</h2>
This image has the latest release of CentOS 8 and contains some modifications for `systemd` operation. The CentOS 8 image comes
from the official CentOS [hub](https://hub.docker.com/_/centos) on Docker Hub.

The image also includes a default user config for `tower` and installs the following supplemental tools:

~~~
ncurses
glibc-locale-source
nano
tcpdump
initscripts
openssh-server
sudo
openssh-clients
net-tools
telnet
glibc-langpack-en
unzip
passwd
yum-utils
authconfig
~~~

The `tower` user has `sudo` rights and has a default password of `test1234`. Please be aware of the default configuration and its potential security implications.
