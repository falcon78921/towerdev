<h1>CentOS 7 systemd Container</h1>

<h2>Purpose:</h2>
This image has the latest release of CentOS 7 and contains some modifications for `systemd` operation. The CentOS 7 image comes
from the official CentOS [hub](https://hub.docker.com/_/centos) on Docker Hub.

The image also includes a default user config for `tower` and installs the following supplemental tools:

~~~
nano
tcpdump
initscripts
openssh-server
sudo
openssh-clients
net-tools
telnet
authconfig
~~~

The `tower` user has `sudo` rights and has a default password of `test1234`. Please be aware of the default configuration and its potential security implications.
