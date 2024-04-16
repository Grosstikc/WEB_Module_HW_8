import mongoengine
from mongoengine import Document, StringField, ListField, ReferenceField, connect

connect(db='authors_quotes_db', host='localhost', port=27017)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=mongoengine.CASCADE)
    quote = StringField()
