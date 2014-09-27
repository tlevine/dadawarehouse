import sqlalchemy as s
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgres import CIDR

from doeund import Fact, Dimension, Column

class URI(Dimension):
    uri = Column(s.String, primary_key = True)

  # To be generated automatically
  # scheme =
  # host =
  # route =
  # query_params = # http://www.postgresql.org/docs/9.3/static/functions-json.html

class Topic(Dimension):
