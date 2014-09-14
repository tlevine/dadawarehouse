import os, shutil
import datetime
from collections import defaultdict

from sqlalchemy import create_engine

from .model import AccountType, Section, Account, \
                   Transaction, GnuCashSplit

def update(session):
    for table in [GnuCashSplit, Transaction, AccountType, Section, Account]:
        session.query(table).delete()
    engine = get_engine()

    account_network = get_account_network(engine)
    session.add_all(accounts(engine, account_network))

    session.add_all(transactions(engine))
    Transaction.create_related(session)

    session.add_all(splits(engine))
    GnuCashSplit.create_related(session)

    session.commit()

def splits(engine):
    sql = 'SELECT guid, account_guid, tx_guid, memo, value_num, value_denom FROM splits'
    for guid, account_guid, transaction_guid, memo, value_num, value_denom in engine.execute(sql).fetchall():
        yield GnuCashSplit(guid = guid,
                           account_guid = account_guid,
                           transaction_guid = transaction_guid,
                           memo = memo,
                           value = value_num / value_denom,
                           value_num = value_num,
                           value_denom = value_denom)

def transactions(engine):
    sql = 'SELECT guid, currency_guid, post_date, enter_date, description FROM transactions'
    for guid, currency_guid, post_date, enter_date, description in engine.execute(sql).fetchall():
        yield Transaction(guid = guid,
                          currency = currency_guid,
                          post_date_id = _parse_date(post_date),
                          enter_date_id = _parse_date(enter_date),
                          description = description)

def accounts(engine, account_network):
    sql = 'SELECT guid, name FROM accounts'
    name_mapping = dict(engine.execute(sql).fetchall())

    sql = '''
SELECT name, code, description, commodity_guid
FROM accounts
WHERE guid = ?
'''
    account_types = {None: None}
    sections = {None: None}
    for account_type, section, account in get_hierarchy(account_network):
        if account == None:
            # A root account
            continue

        name, code, description, cguid = engine.execute(sql, account).fetchone()

        if account_type not in account_types:
            account_types[account_type] = AccountType(
                guid = account_type, account_type = name_mapping[account_type])

        if section not in sections:
            sections[section] = Section(
                guid = section, section = name_mapping[section])

        yield Account(guid = account,
                      name = name,
                      code = code,
                      description = description,
                      commodity_guid = cguid,
                      account_type = account_types[account_type],
                      section = sections[section])

def get_hierarchy(account_network):
    network, placeholders = account_network
    for account_type in network[None]:
        if account_type not in network and account_type not in placeholders:
            yield None, None, account_type
        else:
            for section in network[account_type]:
                if section not in network and section not in placeholders:
                    yield account_type, None, section
                else:
                    for account in network[section]:
                        if account not in network and account not in placeholders:
                            yield account_type, section, account
                        else:
                            raise ValueError('The account with GUID %s does not fit in the three-tier hierarchy.' % account)

            


def get_engine(path = os.path.expanduser('~/safe/finances/finances.gnucash')):
    shutil.copy(path, '/tmp/gnucash.db')
    return create_engine('sqlite:////tmp/gnucash.db')

def get_account_network(engine):
    account_network = defaultdict(lambda: set())
    placeholders = set()

    sql = 'SELECT guid FROM accounts WHERE parent_guid IS NULL'
    root_guid = engine.execute(sql).fetchone()[0]

    sql = 'select parent_guid, guid, placeholder from accounts'
    for parent_guid, guid, placeholder in engine.execute(sql).fetchall():
        account_network[parent_guid].add(guid)
        if placeholder == 1:
            placeholders.add(guid)

    # Remove the root account
    if len(account_network[None]) == 1:
        raise ValueError("I couldn't find the root account.")
    else:
        for root_account in account_network[None]:
            account_network[None] = account_network[None].union(account_network[root_account])
            del(account_network[root_account])

    return dict(account_network), placeholders

def _parse_date(raw):
    return datetime.datetime.strptime(raw, '%Y%m%d%H%M%S')
