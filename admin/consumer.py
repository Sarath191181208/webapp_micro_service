import os

import pika
import django
from django.http.response import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

RABBIT_MQ_URL = "amqps://aygsuifi:CJLlLZquYmEdibi0jMExkEtq8i0S46fX@puffin.rmq2.cloudamqp.com/aygsuifi"
QUEUE = "admin"

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_MQ_URL))
channel = conn.channel()
channel.queue_declare(queue=QUEUE)


def callback(ch, method, props, body):
    print("Received in admin")
    print(body)
    id = json.loads(body)
    print(id)
    product: Product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print("product likes increased!")


channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

print("Started consuming...")

channel.start_consuming()

channel.close()
