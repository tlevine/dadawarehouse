

def load_notmuch(session):
    name_addresses = session.query(NotmuchMessage.from_name,
                                   NotmuchMessage.from_address).distinct()
    for name, address in name_addresses:
        person = session.query(Person)\
                        .join(EmailAddress)\
                        .filter(EmailAddress.emailaddress == address)\
                        .first()
        person.email_addresses = set(person.email_addresses).union({address})
        person.names = set(person.names).union({name})
        session.flush()
