Basic vault / consul docker-compose

6 node consul
3 vault instances

#For local vault development
export VAULT_ADDR=http://127.0.0.1:8200

#For local consul development
export CONSUL_HTTP_ADDR=http://127.0.0.1:8500

#backup / restore unless using state
consul snapshot save backup.snap
consul snapshot restore backup.snap
