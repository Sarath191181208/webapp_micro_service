import json
import pika

RABBIT_MQ_URL = "amqps://aygsuifi:CJLlLZquYmEdibi0jMExkEtq8i0S46fX@puffin.rmq2.cloudamqp.com/aygsuifi"

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_MQ_URL))
channel = conn.channel()


def publish(method, body):
    props = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="admin", body=json.dumps(body), properties=props
    )
