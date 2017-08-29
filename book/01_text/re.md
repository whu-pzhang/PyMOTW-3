# re

>**目的**： 使用正则模式来搜寻和改变文本

正则表达式是用正式语法描述的文本匹配模式。


## 查找文本中的patterns

`re` 最常见的用法便是搜寻文本中的pattern。`search()` 函数以pattern和要扫描的文本为参数，
成功匹配则返回一个`Match`对象，否则返回 `None`。

函数语法如下：

```python
re.search(pattern, string, flags=0)
```

每个 `Match` 对象中包含有匹配的信息，包括输入字符串，匹配的正则表达式以及成功匹配的位置。

```python
# re_simple_match.py

import re

pattern = 'this'
text = 'Does this text match the pattern?'

match = re.search(pattern, text)

s = match.start()
e = match.end()

print('Found "{}"\nin "{}"\nfrom {} to {} ("{}")'.format(
    match.re.pattern, match.string, s, e, text[s:e]))
```


`start()` 和 `end()` 方法返回成功匹配的字符在输入字符串中的索引值。

    $ python3 re_simple_match.py
    Found "this"
    in "Does this text match the pattern?"
    from 5 to 9 ("this")

## 编译正则表达式(Compiling Expressions)

虽然 `re` 包含使用正则表达式作为文本字符串的模块级函数，但编译程序经常使用的正则表达式更为高效。
`compile()` 函数将正则表达式字符转换为 `RegexObject`。

``` python
# re_simple_compiled.py

import re

# Precompile the patterns
regexes = [
    re.compile(p) for p in ['this', 'that']
]

text = 'Does this text match the pattern?'

print('Text: {!r}\n'.format((text)))

for regex in regexes:
    print("Seeking '{}' ->".format(regex.pattern))

    if regex.search(text):
        print("match!")
    else:
        print("no match")
```

模块级功能维护编译正则式的缓存，但高速缓存的大小是有限的，此外使用编译的正则表达式可以避免直接与
高速缓存查找相关联的开销。使用编译好的正则表达式的另外一个好处在于，在加载模块时，预编译所有
正则表达式，编译工作将转移到应用程序开始时，而不是在程序可能响应用户操作的时刻发生。

    $ python3 re_simple_cimpiled.py
    Text: 'Does this text match the pattern?'

    Seeking 'this' ->
    match!
    Seeking 'that' ->
    no match

## 多重匹配

目前为止，我们用到的例子中都只是利用`search()`来匹配文本字符串中的单个实例。
`findall()`函数不重叠的返回与模式相匹配的所有子字符串。

``` python
# re_findall.py

import re

text = "abbaaabbbbaaaaa"

pattern = "ab"

for match in re.findall(pattern, text):
    print("Found {!r}".format(match))
```

该例中，输入字符串包含`'ab'`的两个实例。

    $ python3 re_findall.py
    Found 'ab'
    Found 'ab'

`finditer()` 函数相比`findall()` 返回生成`Match` 实例的迭代器，而不是子字符串。

``` python
# re_finditer.py

import re

text = "abbaaabbbbaaaaa"

pattern = "ab"

for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print("Found {!r} at {:d}:{:d}".format(text[s:e], s, e))
```

上述例子同样在输入字符串中成功匹配到了两处`'ab'`，`Match` 实例显示了其在
原始字符串中的位置。

    $ python3 re_finditer.py
    Found 'ab' at 0:2
    Found 'ab' at 5:7


## Pattern 语法
