# string - Text Constants and Templates

>**目的**：学习用于文本处理的常量和类

`string` 模块可以追溯到最早期版本的Python。以前在此模块中实现的许多功能已被转移为str对象的方法了。
`string`模块保留了用于处理`str`对象的几个有用的常量和类。本部分将集中讨论它们。


## 函数

`capwords()` 函数将字符串中的单词都变为大写开头

```python
# string_capwords.py
import string

s = "The quick brown fox jumped over the lazy dog."
print(s)
print(string.capwords(s))
```

这和先调用`split()`，然后将每个单词首字母大写，最后再用 `join()` 方法将每个单词连接起来得到的结果是一样的。

    $ python3 string_capwords.py
    The quick brown fox jumped over the lazy dog.
    The Quick Brown Fox Jumped Over The Lazy Dog.


## Templates

字符串模板在[PEP 292](https://www.python.org/dev/peps/pep-0292/)中添加，旨在代替内建的内插语法。

使用`string.Template`内插，变量以美元符号 `$`（例如`$var`）前缀来标识。同样的，利用花括号可以将变量和周围的文本区分开来(`${var}`)


```python
# string_template.py

import string

values = {'var': 12.2}

t = string.Template("""
Variable        :$var
Escape          : $$
Variable in text: ${var}iable
""")

print('TEMPLATE:', t.substitute(values))

s = """
Variable        :%(var)s
Escape          : %%
Variable in text: %(var)siable
"""

print('INTERPOLATION:', s % values)

s = """
Variable        : {var}
Escape          : {{}}
Variable in text: {var}iable
"""

print('FORMAT:', s.format(**values))
```

在前两种情况下，触发字符（`$`或`％`）通过重复两次来转义。对于格式化语法，`{`和`}`也需要通过重复它们进行转义。

    $ python3 string_template.py
    TEMPLATE: 
    Variable        :12.2
    Escape          : $
    Variable in text: 12.2iable
    
    INTERPOLATION: 
    Variable        :12.2
    Escape          : %
    Variable in text: 12.2iable
    
    FORMAT: 
    Variable        : 12.2
    Escape          : {}
    Variable in text: 12.2iable
    

模板与字符串插值和格式化之间的一个主要区别在于其不考虑参数的类型。值被转换为字符串直接插入，没有格式化选项。这样就不能控制浮点数的小数位数。

好处在于，利用 `safe_substitute()` 方法可以避免由于模板所需的值和参数提供的值不匹配所引发的异常。


```python
# string_template_missing.py

import string

values = {'var': 'foo'}

t = string.Template("$var is here but $missing is not provited")

try:
    print("substitute()  :", t.substitute(values))
except KeyError as err:
    print("ERROR:", str(err))
    
print("safe_substitute():", t.safe_substitute(values))
```

由于字典中没有 `missing` 对应的值，`substitute()` 抛出了 `KeyError` 异常。

`safe_subtitute()`方法则是捕获了错误而没有抛出，并在文本中将没有键值的表达式保留。

    $ python3 string_template_missing.py
    ERROR: 'missing'
    safe_substitute(): foo is here but $missing is not provited



## 高级Templates

可以通过调整用于在模板中查找变量名的正则表达式模式来更改`string.Template`的默认语法。
最简单的方法就是改变 `delimiter` 和 `idpattern` 这两个类属性。


```python
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
```

此例中，我们改变了替换规则，分隔符由`$`改成了`%`，并且变量名必须包含有下划线。
`%notunderscore`没有被替换就是因为其中不含下划线。

    $ python3 string_template_advanced.py
    Modified ID pattern:
    
      Delimiter  : %
      Replaced   : replaced
      Ignored    : %notunderscore
    
对于更复杂的更改，可以覆盖`pattern`属性并定义一个全新的正则表达式。
提供的模式必须包含四个命名组，用于捕获转义的分隔符，命名变量，变量名称的支持版本以及无效的分隔符模式.

```python
# string_template_defaultpattern.py

import string

t = string.Template("$var")
print(t.pattern.pattern)

```

`t.pattern`的值是一个编译的正则表达式，但原始字符串可通过其`pattern`属性获取。

    $ python3 string_template_defaultpattern.py
        \$(?:
          (?P<escaped>\$) |   # Escape sequence of two delimiters
          (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
          {(?P<braced>[_a-z][_a-z0-9]*)}   |   # delimiter and a braced identifier
          (?P<invalid>)              # Other ill-formed delimiter exprs
        )

下面的示例使用`{{var}}`作为变量语法定义了新的 pattern 来创建新类型的模板。

``` python
# string_template_newsyntax.py

import re
import string


class MyTemplate(string.Template):
    delimiter = "{{"
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''


t = MyTemplate('''
{{{{
{{var}}
''')

print("MATCHES:", t.pattern.findall(t.template))
print("SUBSTITUTED:", t.safe_substitute(var="replacement"))
```

命名和包围的pattern必须分别提供，即使它们完全一样。运行上面例子得到下面的输出：

    $ python3 string_template_newsyntax.py
    MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
    SUBSTITUTED:
    {{
    replacement

## 格式化类(Formatter)



