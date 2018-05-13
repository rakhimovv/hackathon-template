#!/usr/bin/env python

import pika

from g2w_models.predictor import Predictor
from g2w_rabbitmq.config import RPC_QUEUE


def on_request(ch, method, props, body):
    message = body.decode("utf-8")
    print(" [x] Received {}".format(message))

    response = clf.predict(message)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    global clf
    clf = Predictor()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RPC_QUEUE, durable=True, auto_delete=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=RPC_QUEUE)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


if __name__ == '__main__':
    main()
