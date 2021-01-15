# Install Ansible Tower in CentOS 8 Container

FROM centos8/systemd
WORKDIR /opt

# Docker variables
ARG TOWER_VERSION

# Install dependencies & added extras
RUN yum install -y --nogpgcheck ncurses glibc-locale-source nano tcpdump initscripts openssh-server sudo openssh-clients net-tools jq telnet yum glibc-langpack-en unzip passwd yum-utils authconfig tree

# Download & install the specified Ansible Tower version
# if..elif..else statement accounts for oddities in release structure
RUN if [ "$TOWER_VERSION" = "3.3.3" ]; then \
        curl -O https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-${TOWER_VERSION}-1.el7.tar.gz; \
        mv ansible-tower-setup-bundle-${TOWER_VERSION}-1.el7.tar.gz \
        ansible-tower-setup-${TOWER_VERSION}-1.tar.gz; \
    elif [ "$TOWER_VERSION" = "3.7.0" ]; then \
        curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-${TOWER_VERSION}-4.tar.gz; \
        mv ansible-tower-setup-${TOWER_VERSION}-4.tar.gz \
        ansible-tower-setup-${TOWER_VERSION}-1.tar.gz; \
    else \
        curl -O https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-${TOWER_VERSION}-1.tar.gz; \ 
    fi
RUN tar -xvf ansible-tower-setup-${TOWER_VERSION}-1.tar.gz

# if..elif..else statement accounts for oddities in packaging structure
RUN if [ "$TOWER_VERSION" = "3.3.3" ]; then \
        mv ansible-tower-setup-bundle-${TOWER_VERSION}-1.el7 ansible-tower-setup-${TOWER_VERSION}-1; \
    elif [ "$TOWER_VERSION" = "3.7.0" ]; then \
        mv ansible-tower-setup-3.7.0-4 ansible-tower-setup-3.7.0-1; \
    fi
RUN rm ansible-tower-setup-${TOWER_VERSION}-1.tar.gz

# Let's create a directory for inventory data
RUN mkdir -p tower_inventory

# Copy inventory files into tower_inventory/
COPY inventory/* /opt/tower_inventory/

# Place redhat-uep.pem inside /etc/rhsm/ca (for subscription activation)
RUN mkdir -p /etc/rhsm/ca
COPY misc/redhat-uep.pem /etc/rhsm/ca

# Assign inventory based on version
RUN if [[ "$TOWER_VERSION" = *3.5* ]]; then \
        cp tower_inventory/inventory_3.5.x \
        ansible-tower-setup-${TOWER_VERSION}-1/inventory; \
        cp tower_inventory/cluster_inventory_3.5.x \
        ansible-tower-setup-${TOWER_VERSION}-1/cluster_inventory_3.5.x; \
    elif [[ "$TOWER_VERSION" = *3.6* ]]; then \
        cp tower_inventory/inventory_3.6.x \
        ansible-tower-setup-${TOWER_VERSION}-1/inventory; \
        cp tower_inventory/cluster_inventory_3.6.x \
        ansible-tower-setup-${TOWER_VERSION}-1/cluster_inventory_3.6.x; \
    elif [[ "$TOWER_VERSION" = *3.7* ]]; then \
        cp tower_inventory/inventory_3.7.x \
        ansible-tower-setup-${TOWER_VERSION}-1/inventory; \
        cp tower_inventory/cluster_inventory_3.7.x \
        ansible-tower-setup-${TOWER_VERSION}-1/cluster_inventory_3.7.x; \
    elif [[ "$TOWER_VERSION" = *3.8* ]]; then \
        cp tower_inventory/inventory_3.8.x \
        ansible-tower-setup-${TOWER_VERSION}-1/inventory; \
        cp tower_inventory/cluster_inventory_3.8.x \
        ansible-tower-setup-${TOWER_VERSION}-1/cluster_inventory_3.8.x; \
    fi

# Set permissions on setup.sh & enable sshd
RUN chmod +x /opt/ansible-tower-setup-${TOWER_VERSION}-1/setup.sh
RUN systemctl enable sshd.service

# Finish it!
CMD ["/usr/sbin/init"]
