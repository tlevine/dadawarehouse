import os

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Date

import doeund as m

class PalFile(m.Dimension):
    pk = m.Column(String(2), primary_key = True, label = 'Two-letter code')
    filename = m.Column(String, unique = True, label = 'File name')
    description = m.Column(String)

class PalEvent(m.Fact):
    pk = m.PkColumn(hide = True)
    file_id = m.Column(String(2), ForeignKey(PalFile.pk))
    file = relationship(PalFile)
    date = m.Column(Date)
    description = m.Column(String)
