# CentOS 7 SSH systemd Container (with some extras)

FROM centos:7
WORKDIR /opt

# Install systemd 
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

# Install dependencies & added extras
RUN yum install -y nano tcpdump initscripts openssh-server sudo openssh-clients net-tools telnet authconfig
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Create SSH-able user
RUN useradd tower
RUN echo "test1234" | passwd tower --stdin

# Update sudoers config
COPY sudoers/tower /etc/sudoers.d

# Activate SSH service
RUN systemctl enable sshd.service

# Finish it!
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
