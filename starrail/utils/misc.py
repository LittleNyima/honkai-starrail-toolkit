import functools
import importlib


@functools.lru_cache
def lazy_import(name, package=None):
    return importlib.import_module(name, package)
