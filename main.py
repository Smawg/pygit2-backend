#!/usr/bin/env python3

"""Initial tests for git as data backend. Creates a data storage, which prints the location of the git repository. Then sleeps forever.
"""

from datastore import Datastore
import time

if __name__=='__main__':
    with Datastore() as ds:
        ds.addTransaction(2016, 'test')
        while True:
            time.sleep(2)
