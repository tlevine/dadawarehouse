import os, shutil
import datetime
from collections import defaultdict

from sqlalchemy import create_engine

from ..logger import logger
from .model import Account, Transaction, Split

def update(sessionmaker):
    session = sessionmaker()
    for table in [Split, Transaction, Account]:
        session.query(table).delete()
    engine = get_engine()
    account_network = get_account_network(engine)

    session.add_all(accounts(engine, account_network))
    logger.info('Added GnuCash accounts')
    session.add_all(transactions(engine))
    logger.info('Added GnuCash transactions')
    session.commit()

    session.add_all(splits(engine))
    logger.info('Added GnuCash splits')
    session.commit()
    logger.info('Finished loading GnuCash')

def splits(engine):
    sql = 'SELECT guid, account_guid, tx_guid, memo, value_num, value_denom FROM splits'
    for guid, account_guid, transaction_guid, memo, value_num, value_denom in engine.execute(sql):
        yield Split(guid = guid,
                    account_guid = account_guid,
                    transaction_guid = transaction_guid,
                    memo = memo,
                    value = value_num / value_denom,
                    value_num = value_num,
                    value_denom = value_denom)

def transactions(engine):
    sql = 'SELECT guid, currency_guid, post_date, enter_date, description FROM transactions'
    for guid, currency_guid, post_date, enter_date, description in engine.execute(sql):
        yield Transaction(guid = guid,
                          currency = currency_guid,
                          post_date = _parse_date(post_date),
                          enter_date = _parse_date(enter_date),
                          description = description)

def accounts(engine, account_network):
    sql = 'SELECT guid, name FROM accounts'
    name_mapping = {k:v for k,v in engine.execute(sql)}

    sql = '''
SELECT name, code, description, commodity_guid
FROM accounts
WHERE guid = ?
'''
    for account_type, section, account in get_hierarchy(account_network):
        if account == None:
            # A root account
            continue

        name, code, description, cguid = engine.execute(sql, account).fetchone()

        yield Account(guid = account,
                      name = name,
                      code = code,
                      description = description,
                      commodity_guid = cguid,
                      account_type = name_mapping.get(account_type),
                      section = name_mapping.get(section))

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
    root_guids = set(row[0] for row in engine.execute(sql))

    sql = 'select parent_guid, guid, placeholder from accounts WHERE parent_guid NOT NULL'
    for parent_guid, guid, placeholder in engine.execute(sql):
        if parent_guid in root_guids:
            parent_guid = None
        account_network[parent_guid].add(guid)
        if placeholder == 1:
            placeholders.add(guid)

    return dict(account_network), placeholders

def _parse_date(raw):
    return datetime.datetime.strptime(raw, '%Y%m%d%H%M%S')
