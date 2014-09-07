#!/usr/bin/env python3
import json

import sqlalchemy

from doeund import create

# Load the schema.
import warehouse.pal.model

engine = sqlalchemy.create_engine("sqlite:///")
session, model = create(engine)
with open('/tmp/model.json', 'w') as fp:
    json.dump(model, fp)
