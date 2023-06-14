import functools
import hashlib
import importlib


@functools.lru_cache
def lazy_import(name, package=None):
    return importlib.import_module(name, package)


@functools.lru_cache
def sha1(data):
    hasher = hashlib.sha1()
    if isinstance(data, str):
        data = data.encode('utf-8')
    hasher.update(data)
    return hasher.hexdigest()
