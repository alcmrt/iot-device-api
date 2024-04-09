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
        #print(f" [x] Received {body}")
        
        message = json.loads(body) # get message from queue as json object
        print("message:", message)
        print(type(message))

        url = ''
        headers = {"content-type": "application/json"}
        payload = json.dumps({ "name": message, "data": { "color": "white", "generation": "3rd", "price": 135}})

        # send data to our api
        #response = requests.post(url, json = myobj, headers=headers)
        #print(response.text)
        
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
