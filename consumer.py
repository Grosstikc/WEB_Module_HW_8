import pika
from mongoengine import connect, Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField()

connect(db='contact_db', host='localhost', port=27017)

def callback(ch, method, properties, body):
    contact = Contact.objects(id=body.decode()).first()
    if contact and not contact.message_sent:
        print(f"Sending email to {contact.email}")
        contact.message_sent = True
        contact.save()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
