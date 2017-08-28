# string_template_advanced.py

import string


class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = "[a-z]+_[a-z]+"


template_text = """
  Delimiter  : %%
  Replaced   : %with_underscore
  Ignored    : %notunderscore
"""

d = {
    'with_underscore': 'replaced',
    'notunderscore': 'not replaced'
}

t = MyTemplate(template_text)
print('Modified ID pattern:')
print(t.safe_substitute(d))
