#!/usr/bin/python3

#
#This is a dev instance I don't care if you see the token o ye ruthless github scanners ;)
#

import requests
import pika
vault_server = 'http://10.10.10.44:8200'
token = '4myVrzAJrUqWIAQ06nPoWyRV'
role_id = 'de833b87-6f41-f089-38b0-6d5932a32e3c'

#need to get secret-id
secret_id_url = vault_server + '/v1/auth/approle/role/rabbit-approle/secret-id'
headers = {'X-Vault-Token': token}
r = requests.post(secret_id_url, headers=headers)
secret_id = r.json()['data']['secret_id']

#Then need to create token with role_id + secret_id
token_url = vault_server + '/v1/auth/approle/login'
r = requests.post(token_url, json={'role_id':role_id, 'secret_id':secret_id})
approle_token = r.json()['auth']['client_token']

#Now need to create the dynamic cred with this token
rabbit_cred_url = vault_server + '/v1/rabbitmq/creds/rabbit-role'
headers = {'X-Vault-Token': approle_token}
r = requests.get(rabbit_cred_url, headers=headers)

un = r.json()['data']['username']
pw = r.json()['data']['password']

#Now can use this dynamically created un/pw to do whatever it is authorized to do in rabbitmq

credentials = pika.PlainCredentials(un, pw)
connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.10.44', credentials=credentials, port='5672', virtual_host='/'))

channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()
