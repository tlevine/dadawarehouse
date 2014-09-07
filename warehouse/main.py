import os
import json

from sqlalchemy import create_engine

import doeund

from warehouse.history.load import update as history
from warehouse.pal.load import update as pal
from warehouse.facebookchat.load import update as fb
from warehouse.twitter.load import update as twitter

CACHE_DIRECTORY = os.path.expanduser('~/.dadawarehouse')

def load_data():
  # engine = create_engine('postgres:///tlevine')
    engine = create_engine('sqlite:////tmp/dada.sqlite')
    session = doeund.database(engine)
    fb(session)
    history(session)
    pal(session)

def export_model():
    engine = create_engine("sqlite:///")
    model = doeund.model()
    with open('/tmp/model.json', 'w') as fp:
        json.dump(model, fp, indent = 2, separators = (',', ': '))
