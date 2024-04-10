"""
Implementation of simple RabbitMQ receiver.
Receives IoT GPS data into queue then send the data through our API to write database.

In order to start the receiver run 'python receive.py' command.
"""

import json
import pika, sys, os, time
import requests

def main():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='iot')

    def callback(ch, method, properties, body):
        """
        Triggers when a message received. 
        Gets message from queue and send the message to our API 
        """
        
        # get message from queue as json object
        message = json.loads(body)

        #print("message:", message)
        #print(type(message))

        # request information
        url = 'http://localhost:8000/devices'
        headers = {"content-type": "application/json"}

        # send data to our api
        response = requests.post(url, json = message, headers=headers)
        print(response.text)
        
    channel.basic_consume(queue='iot', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
