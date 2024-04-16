import pika
from mongoengine import connect, Document, StringField, BooleanField
from faker import Faker

fake = Faker()

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

connect(db='contact_db', host='localhost', port=27017)

def send_to_queue(contact_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')
    channel.basic_publish(exchange='',
                          routing_key='email_queue',
                          body=contact_id)
    connection.close()

for _ in range(10):  # Generate 10 fake contacts
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        message_sent=False
    )
    contact.save()
    send_to_queue(str(contact.id))
