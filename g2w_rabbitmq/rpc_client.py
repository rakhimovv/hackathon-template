#!/usr/bin/env python
import time

import pika
import uuid

from pika.exceptions import ConnectionClosed

from g2w_rabbitmq.config import RPC_QUEUE


class RpcClient(object):
    def __init__(self):
        self.__connect()

    def __connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        while True:
            try:
                self.channel.basic_publish(exchange='',
                                           routing_key=RPC_QUEUE,
                                           properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                           correlation_id=self.corr_id,
                                                                           delivery_mode=2),
                                           body=body)
                break
            except ConnectionClosed:
                print('oops. lost connection. trying to reconnect.')
                # avoid rapid reconnection on longer RMQ server outage
                time.sleep(0.5)
                self.__connect()
        while self.response is None:
            self.connection.process_data_events()
        return self.response
