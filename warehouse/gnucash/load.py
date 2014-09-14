from collections import defaultdict

from .model import AccountType, Section, Account, \
                   Transaction, GnuCashSplit

def update(session):
    engine = get_engine()

    account_network = get_account_network(engine)
    session.add_all(accounts(account_network))

    session.add_all(transactions(engine))
    Transaction.create_related(session)

def transactions(engine)
    sql = 'SELECT guid, currency_guid, post_date, enter_date, description FROM transactions'
    for guid, currency_guid, post_date, enter_date, description in engine.execute(sql).fetchall():
        yield Transaction(guid = guid,
                          currency = currency_guid,
                          post_date_id = parse_date(post_date),
                          enter_date_id = parse_date(enter_date),
                          description = description)

def accounts(account_network):
    sql = 'SELECT guid, name FROM accounts'
    name_mapping = dict(engine.execute(sql).fetchall())

    sql = '''
SELECT name, code, description, commodity_guid
FROM accounts
WHERE guid = ?
'''
    for account_type, section, account in get_hierarchy(account_network):
        name, code, description, cguid = engine.execute(sql, guid).fetchone()
        account_type = AccountType(guid = account_type,
                                   account_type = name_mapping[account_type])
        section = Section(guid = section,
                          section = name_mapping[section])
        yield Account(name = name,
                      code = code,
                      description = description,
                      commodity_guid = cguid,
                      account_type = account_type,
                      section = section)

def get_hierarchy(account_network):
    network, placeholders = account_network
    for account_type in network.keys():
        if len(network[account_type]) == 0 and account_type not in placeholders:
            yield None, None, account_type
        else:
            for section in network[account_type]:
                if len(network[section]) == 0 and section not in placeholders:
                    yield account_type, None, section
                else:
                    for account in network[section]:
                        if len(network[account]) == 0 and account not in placeholders:
                            yield account_type, section, account
                        else:
                            raise ValueError('The account with GUID %s does not fit in the three-tier hierarchy.' % account)

            


def get_engine(path = os.path.expanduser('~/safe/finances/finances.gnucash')):
    shutil.copy(path, '/tmp/gnucash.db')
    return sqlalchemy.create_engine('sqlite:////tmp/gnucash.db')

def get_account_network(engine)
    account_network = defaultdict(lambda: set())
    placeholders = set()
    sql = 'select parent_guid, guid, placeholder from accounts'
    for parent_guid, guid, placeholder in engine.execute(sql).fetchall():
        account_network[parent_guid].add(guid)
        if placeholder:
            placeholders.add(guid)
    return account_network, placeholders
