[tower]


[database]

[all:vars]
admin_password='redhat'

pg_host='<POSTGRES_SERVER>'
pg_port='<POSTGRES_PORT>'

pg_database='awxclusterXXX'
pg_username='<POSTGRES_USERNAME>'
pg_password='<POSTGRES_PASSWORD>'
pg_sslmode='prefer'  # set to 'verify-full' for client-side enforced SSL

# Isolated Tower nodes automatically generate an RSA key for authentication;
# To disable this behavior, set this value to false
# isolated_key_generation=true


# SSL-related variables

# If set, this will install a custom CA certificate to the system trust store.
# custom_ca_cert=/path/to/ca.crt

# Certificate and key to install in nginx for the web UI and API
# web_server_ssl_cert=/path/to/tower.cert
# web_server_ssl_key=/path/to/tower.key

# Server-side SSL settings for PostgreSQL (when we are installing it).
# postgres_use_ssl=False
# postgres_ssl_cert=/path/to/pgsql.crt
# postgres_ssl_key=/path/to/pgsql.key

