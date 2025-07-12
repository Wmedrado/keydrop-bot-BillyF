class _Cred:
    def __init__(self, path):
        self.path = path

class credentials:
    Certificate = _Cred

def initialize_app(*args, **kwargs):
    return object()

class _DBRef:
    def get(self):
        return {}
    def update(self, data):
        pass
    def child(self, name):
        return _DBRef()
    def set(self, value):
        pass

class _DB:
    def reference(self, path):
        return _DBRef()

db = _DB()

class _Blob:
    def upload_from_filename(self, fn):
        pass
    def make_public(self):
        pass
    @property
    def public_url(self):
        return ""

class _Bucket:
    def blob(self, name):
        return _Blob()

class _Storage:
    def bucket(self):
        return _Bucket()

storage = _Storage()

from . import auth
