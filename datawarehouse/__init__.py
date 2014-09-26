import csv

from sqlalchemy.orm import sessionmaker

from .person import Person, Facebook, Twitter, Name, EmailAddress, IPAddress

file_mapping = [
    ('person.csv', Person),
    ('facebook.csv', Facebook),
    ('name.csv', Name),
    ('emailaddress.csv', EmailAddress),
    ('ipaddress.csv', IPAddress),
]
def load(directory, engine):
    session = sessionmaker(bind=engine)()
    for filename, Class in file_mapping:
        with open(os.path.join(directory, filename)) as fp:
            reader = csv.DictReader(fp)
            session.add_all(Class(**row) for row in reader)
    session.commit()
