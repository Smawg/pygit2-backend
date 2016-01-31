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

        try:
            commit = self.git_repo.revparse_single('HEAD')
        except KeyError as ke:
            self._createInitCommit()

        print(self.git_repo_path)

    def _createInitCommit(self):
        blob = self.git_repo.create_blob('# Datastore for SMAWG\n')
        tree = self.git_repo.TreeBuilder()
        tree.insert('README.md', blob, pygit2.GIT_FILEMODE_BLOB)
        author = pygit2.Signature('Niklas Claesson', 'niklas@smawg.se')
        comitter = author
        self.git_repo.create_commit(
                'refs/heads/master', 
                author, 
                comitter, 
                'Initialize repository', 
                tree.write(),
                []
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.git_repo_path:
            shutil.rmtree(self.git_repo_path)

    def _createYear(self, year):
        blob = self.git_repo.create_blob('{}\n'.format(json.dumps('init')))
        parent_commit = self.git_repo.lookup_reference('HEAD').get_object()
        tree = self.git_repo.TreeBuilder(parent_commit.tree)
        tree.insert('{}'.format(year), blob, pygit2.GIT_FILEMODE_BLOB)
        author = pygit2.Signature('Niklas Claesson', 'niklas@smawg.se')
        comitter = author
        self.git_repo.create_commit(
                'refs/heads/master',
                author,
                comitter,
                'Add year {}'.format(year),
                tree.write(),
                [parent_commit.id]
                )


    def addTransaction(self, year, something):
        year = str(year)
        master_ref = self.git_repo.lookup_reference('HEAD')
        commit = master_ref.get_object()
        tree = commit.tree
        for entry in tree:
            if entry.name == year:
                break
        else:
            self._createYear(year)
