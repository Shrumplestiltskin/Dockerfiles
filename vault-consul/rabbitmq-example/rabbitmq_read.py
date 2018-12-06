#!/usr/bin/python3

#
#Uses vault to issue a dynamic credential, reads from RabbitMQ, disconnects, then cleans up token
#

import requests
import pika
from os import environ
from sys import exit
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

    def close_and_cleanup():
        #Clean up token
        connection.close()
        revoke_approle_token(approle_token)
        exit(0)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        close_and_cleanup()

    channel.basic_consume(callback, queue='hello', no_ack=True)

    print(' [*] Waiting for message. To exit press CTRL+C')
    channel.start_consuming()
