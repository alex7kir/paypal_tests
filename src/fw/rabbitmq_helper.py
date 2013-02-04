'''
Created on 05.07.2012

@author: akiryuhin
'''
from fw.helper_base import HelperBase
import pika
from pika.spec import BasicProperties
import time

class RabbitmqHelper(HelperBase):

    def __init__(self, manager):
        super(RabbitmqHelper, self).__init__(manager)
        self.connection = None
        self.channel = None
        self.response = None
        
    def establish_connection(self, host, port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = host, port = port))
        self.channel = self.connection.channel()
        return self.connection, self.channel 
        
    def send_message(self, channel, command, msg, from_who, exchange, routing_key, reply_to, response_queue=None, response_routing_key=None):
        headers = {}
        headers['command'] = command
        headers['from'] = from_who
        properties = BasicProperties(headers=headers,content_type = 'application/json', reply_to = reply_to, timestamp=time.time())

        if response_queue:
            channel.queue_declare(queue=response_queue)
            channel.queue_bind( queue = response_queue,
                exchange = exchange,
                routing_key = response_routing_key)

        channel.basic_publish(exchange = exchange, routing_key = routing_key, body = msg, properties = properties)
        
    def receive_nth_response(self, channel, queue, n, no_ack=True):
        self.i = 0
        if n>1:
            self.response={}

        def callback(ch, method, properties, body):
            if n==1:
                self.response=body
            else:
                self.response[self.i] = body
            self.i = self.i + 1
            if self.i == n:
                channel.stop_consuming()
        try:
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback, queue = queue, no_ack=no_ack)
            channel.start_consuming()
        except KeyError: pass

        return self.response
            
    def close_connection(self, connection):
        connection.close()
        
    def get_channel(self):
        return self.channel
        
