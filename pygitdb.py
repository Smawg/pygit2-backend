import pygit2
import tempfile
import os,sys,shutil
import yaml


def create_engine(*args, **kwargs):
    if 'clone_from' in kwargs.keys():
        return Engine(clone_from=kwargs['clone_from'])
    return Engine()


def create_session(bind=None):
    if 'bind' in kwargs.keys():
        return Session(bind=kwargs['bind'])
    return None

class Base(object):
    pass

"""Supported languages: yaml, toml, json, xml"""
class Engine(object):
    git_repo_path = None;
    git_repo = None;

    def __init__(self, clone_from=None, lang='yaml'):
        self.git_repo_path = tempfile.mkdtemp()
        if clone_from:
            self.git_repo = pygit2.clone_repository(clone_from, self.git_repo_path, bare=True)
        else:
            self.git_repo = pygit2.init_repository(self.git_repo_path, bare=True)

        try:
            commit = self.git_repo.revparse_single('HEAD')
        except KeyError as ke:
            self._create_init_commit()

        print(self.git_repo_path)

    def _get_author(self):
        global_config = pygit2.Config.get_global_config()
        try:
            name = global_config['user.name']
        except KeyError as ke:
            name = '(undefined)'
        try:
            email = global_config['user.email']
        except KeyError as ke:
            email = '(undefined)'

        return pygit2.Signature(name, email)

    def _create_init_commit(self):
        blob = self.git_repo.create_blob('# Datastore for SMAWG\n')
        tree = self.git_repo.TreeBuilder()
        tree.insert('README.md', blob, pygit2.GIT_FILEMODE_BLOB)
        author = self._get_author()
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
        blob = self.git_repo.create_blob('{}\n'.format(yaml.dump('init')))
        parent_commit = self.git_repo.lookup_reference('HEAD').get_object()
        tree = self.git_repo.TreeBuilder(parent_commit.tree)
        tree.insert('{}'.format(year), blob, pygit2.GIT_FILEMODE_BLOB)
        author = self._get_author()
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

class Session(object):
    def __init__(self, bind=engine):
        pass

    def add(obj):
        pass

    def commit():
        pass

