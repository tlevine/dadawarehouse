import sqlalchemy

from doeund import create

# Load the schema.
import warehouse.pal.model

engine = sqlalchemy.create_engine("sqlite:///")
session, model = create(engine)
