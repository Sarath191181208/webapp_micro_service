import json

import pika

from main import Product, db, app

RABBIT_MQ_URL = "amqps://aygsuifi:CJLlLZquYmEdibi0jMExkEtq8i0S46fX@puffin.rmq2.cloudamqp.com/aygsuifi"
QUEUE = "main"

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_MQ_URL))
channel = conn.channel()
channel.queue_declare(queue=QUEUE)


def callback(ch, method, props, body):
    print("Received in main")
    print(body)
    data = json.loads(body)
    print(data)
    with app.app_context():
        if props.content_type == "product_created":
            product = Product(id=data["id"], title=data["name"], image=data["image"])
            db.session.add(product)
        elif props.content_type == "product_updated":
            product = Product.query.get(data["id"])
            if product is None:
                return 
            product.title = data["title"]
            product.image = data["image"]
        elif props.content_type == "product_deleted":
            product = Product.query.get(data["id"])
            db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

print("Started consuming...")

channel.start_consuming()

channel.close()
