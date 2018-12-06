#!/usr/bin/python3

#
#Uses vault to issue a dynamic credential, writes to RabbitMQ, disconnects, then cleans up token
#

import requests
import pika
from os import environ
from rabbitmq_helpers import *

rabbitmq_host = environ['RABBIT_HOST']
token = environ['RABBIT_TOKEN']

if __name__ == '__main__':
    #Vault stuff
    role_id, secret_id = get_approle_ids(token)
    approle_token = create_approle_token(role_id, secret_id)
    un, pw = create_dynamic_credential(approle_token)

    #RabbitMQ Stuff
    credentials = pika.PlainCredentials(un, pw)
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, credentials=credentials, port='5672', virtual_host='/'))

    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

    print(" [x] Sent 'Hello World!'")
    connection.close()

    #Clean up token
    r = revoke_approle_token(approle_token)
