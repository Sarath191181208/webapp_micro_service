import pika

RABBIT_MQ_URL = "amqps://aygsuifi:CJLlLZquYmEdibi0jMExkEtq8i0S46fX@puffin.rmq2.cloudamqp.com/aygsuifi"
QUEUE = "main"

conn = pika.BlockingConnection(pika.URLParameters(RABBIT_MQ_URL))
channel = conn.channel()
channel.queue_declare(queue=QUEUE)


def callback(ch, method, props, body):
    print("Recived in admin: ")
    print(body)

    with open("admin.log", "a") as f:
        f.write(str(body))
        f.write("\n")


channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print("Started consuming...")

channel.start_consuming()

channel.close()
