# string_constants.py

import string
import inspect


def is_str(value):
    return isinstance(value, str)


for name, value in inspect.getmembers(string, is_str):
    if name.startswith('_'):
        continue
    print('{}={!r}\n'.format(name, value))
