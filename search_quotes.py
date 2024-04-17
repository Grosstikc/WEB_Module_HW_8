import mongoengine
from mongoengine import connect
from database_models import Author, Quote

connect(db='authors_quotes_db', host='localhost', port=27017)

def search_by_author(fullname):
    author = Author.objects(fullname=fullname).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(f"{quote.quote}")
    else:
        print("No quotes found for this author.")

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(f"{quote.quote}")

def search_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    for quote in quotes:
        print(f"{quote.quote}")

def main():
    while True:
        command = input("Enter your command (type 'exit' to quit): ")
        if command == "exit":
            break
        key, value = command.split(':', 1)
        value = value.strip()
        if key == 'name':
            search_by_author(value)
        elif key == 'tag':
            search_by_tag(value)
        elif key == 'tags':
            tags = value.split(',')
            search_by_tags(tags)
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
