[tower]


[database]

[all:vars]
ansible_become='true'
ansible_become_method='sudo'
ansible_become_password='test1234'
admin_password='redhat'
ansible_all_ipv6_addresses='false'
ansible_user='tower'
ansible_password='test1234'
ansible_connection='ssh'
ansible_ssh_common_args='-o StrictHostKeyChecking=no'

pg_host='<POSTGRES_SERVER>'
pg_port='<POSTGRES_PORT>'

pg_database='awxclusterXXX'
pg_username='<POSTGRES_USERNAME>'
pg_password='<POSTGRES_PASSWORD>'

rabbitmq_port=5672
rabbitmq_vhost=tower
rabbitmq_username=tower
rabbitmq_password='redhat'
rabbitmq_cookie=cookiemonster
rabbitmq_use_long_name='true'
#rabbitmq_use_ssl='true'

# Isolated Tower nodes automatically generate an RSA key for authentication;
# To disable this behavior, set this value to false
# isolated_key_generation=true
