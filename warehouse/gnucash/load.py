from collections import defaultdict

from .model import GnuCashSplit

def update(session):
    engine = get_engine()
    account_network = get_account_network(engine)
    for account_type, section, account in get_hierarchy(account_network):
        pass


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

guid|name|account_type|commodity_guid|commodity_scu|non_std_scu|parent_guid|code|description|hidden|placeholder
3596d67413d80aa279457356c8323b4a|Root Account|ROOT|962b27c3d3ba3814d77c75089c074ec6|100|0||||0|0
592369efc64bc358250eaed95c053a10|Assets|ASSET|962b27c3d3ba3814d77c75089c074ec6|100|0|3596d67413d80aa279457356c8323b4a||Assets|0|1
a8c94fe5df8e88510e694521d23c58bb|Tompkins Trust|BANK|962b27c3d3ba3814d77c75089c074ec6|100|0|3332dea01b0c1c6685deeca9ce026640||Checking Account at Tompkins Trust|0|0
