from __future__ import print_function
import pygit2
import tempfile
import os,sys,shutil
import json


"""Use 'with Datastore() as ds' to open Datastore"""

class Datastore(object):
    git_repo_path = None;
    git_repo = None;

    def __init__(self, clone_from=None):
        self.git_repo_path = tempfile.mkdtemp()
        if clone_from:
            self.git_repo = pygit2.clone_repository(clone_from, self.git_repo_path, bare=True)
            return self
        self.git_repo = pygit2.init_repository(self.git_repo_path, bare=True)
        print(self.git_repo_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.git_repo_path:
            shutil.rmtree(self.git_repo_path)

    def _createYear(self, year):
        year = str(year)
        ledger_path = os.path.join(self.git_repo_path, year)
        blob = self.git_repo.create_blob('{}\n'.format(json.dumps('init')))
        tree = self.git_repo.TreeBuilder()
        tree.insert('{}'.format(year), blob, pygit2.GIT_FILEMODE_BLOB)
        author = pygit2.Signature('Niklas Claesson', 'niklas@smawg.se')
        comitter = author
        self.git_repo.create_commit(
                'refs/heads/master', 
                author, 
                comitter, 
                'message', 
                tree.write(),
                []
                )


    def addTransaction(self, year, init):
        ledger_path = os.path.join(self.git_repo_path, year)
        if not os.isfile(ledger):
            self._createYear(year_path)
