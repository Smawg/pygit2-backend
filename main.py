from __future__ import print_function
from datastore import Datastore
import time

if __name__=='__main__':
    with Datastore() as ds:
        ds.addTransaction('test')
        while True:
            time.sleep(2)
