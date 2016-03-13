
from pygitdb import create_engine

def test_empty():
    engine = create_engine()
    engine.addTransaction('test')


def test_clone():
    enginge = create_engine(clone_from="git://github.com/smawg/demo-accounting")
    engine.addTransaction('test')
