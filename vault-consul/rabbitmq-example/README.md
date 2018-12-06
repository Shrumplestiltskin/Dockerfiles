#Good refs -   
https://www.rabbitmq.com/tutorials/tutorial-one-python.html   
https://blog.alanthatcher.io/vault-approle-authentication/   
https://www.vaultproject.io/docs/secrets/rabbitmq/index.html    
https://www.vaultproject.io/docs/auth/approle.html   
https://www.vaultproject.io/api/auth/approle/index.html   
https://www.vaultproject.io/api/secret/rabbitmq/index.html   

#Start rabbit instance   
docker run --restart=unless-stopped -p15672:15672 -p5672:5672 -d rabbitmq:3.7-management-alpine   

#Enable rabbitmq secrets engine   
./vault secrets enable rabbitmq    

#Specify host and credentials on RMQ that can create users   
vault write rabbitmq/config/connection connection_uri="http://localhost:15672" username="admin" password="password"   

#Define a rabbit mq role that gets added to a dynamic user   
./vault write rabbitmq/roles/rabbit-role \   
    vhosts='{"/":{"configure": ".*", "write": ".*", "read": ".*"}}'   
	
#Calling this role will create dynamic credentials that give this access on rabbitmq   
#Whatever token issues will be the token whose lifetime is associated   
./vault read rabbitmq/creds/rabbit-role   

#need to create a vault policy that can read the rabbit-role   
path "rabbitmq/creds/rabbit-role" {    
        capabilities = ["read"]   
}   

#create the approle with this policy attached   
./vault write auth/approle/role/rabbit-approle secret_id_ttl=1m secret_id_num_uses=1 token_num_uses=3 token_ttl=10m token_max_ttl=30m policies=rabbit-role-policy   

#create vault policy to get secret-id of rabbit-role   
path "auth/approle/role/rabbit-approle/secret-id" {   
        capabilities = ["update"]   
}   

#get token from this policy   
./vault token create -policy=rabbit-secret-id-policy   

#create approle token with the role_id + secret_id_num_uses   
./vault write auth/approle/login role_id=de833b87-6f41-f089-38b0-6d5932a32e3c secret_id=c513533b-4342-3ad2-de24-4cfdd53e9ece   

#use that token to create the dynamic credentials   
./vault read rabbitmq/creds/rabbit-role   

