
from pygitdb import create_engine

from pygitdb import Base, Entry, Date, Integer, String

class FiscialYear(Base):
    start_date = Entry(Date)
    end_date = Entry(Date)
    charts_of_accounts = Entry(String)
    def __init__(self, year):
        self._filename = os.path.join(year, 'year')

class Transaction(Base):
    def __init__(self, year):
        self._filename = os.path.join(year, 'journal')

class Posting(Base):
    def __init__(self, year):
        self._filename = os.path.join(year, 'journal')

def test_empty():
    engine = create_engine()
    engine.addTransaction('test')


def test_clone():
    enginge = create_engine(clone_from="git://github.com/smawg/demo-accounting")
    engine.addTransaction('test')
