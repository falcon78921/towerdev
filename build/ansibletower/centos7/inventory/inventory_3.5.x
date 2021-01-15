[tower]
localhost ansible_connection=local

[database]

[all:vars]
admin_password='redhat'
ansible_all_ipv6_addresses='false'

pg_host=''
pg_port=''

pg_database='awx'
pg_username='awx'
pg_password='redhat'

rabbitmq_port=5672
rabbitmq_vhost=tower
rabbitmq_username=tower
rabbitmq_password='redhat'
rabbitmq_cookie=cookiemonster
rabbitmq_use_long_name='false'

# Isolated Tower nodes automatically generate an RSA key for authentication;
# To disable this behavior, set this value to false
# isolated_key_generation=true
