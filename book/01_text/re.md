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

print('Text: {!r}\n'.format(text))

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

正则表达式除了字符串匹配，还支持更为强大的模式匹配。
Patterns can repeat, can be anchored to different logical locations within the input, and can be expressed in compact forms that do not require every literal character to be present in the pattern.

所有这些特性

``` python
# re_test_pattern.py

import re


def test_patterns(text, patterns):
    '''
    Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    '''
    # Look for each pattern in the text and print the results
    for pattern, desc in patterns:
        print("'{}' ({})\n".format(pattern, desc))
        print("  '{}'".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = '.' * (s + n_backslashes)
            print("  {}'{}'".format(prefix, substr))

        print()
    return


if __name__ == '__main__':
    test_patterns('abbaaabbbbaaaaa',
                  [('ab', "a followed by 'b'"),
                   ])
```

例子中用`text_patterns()` 函数来声明patterns中的变量如何改变匹配输入字符串的方式。
输出显示了输入文本和成功匹配的每个子字符串的范围。

    $ python3 re_test_pattern.py
    'ab' (a followed by 'b')

    'abbaaabbbbaaaaa'
    'ab'
    .....'ab'

## 重复(Repetition)

在一个匹配模式中有五种方法来表示重复。

| 元字符  |                                       含义                                       |
| :-----: | -------------------------------------------------------------------------------- |
|   `*`   | 匹配前一个字符0或无限次                                                          |
|   `+`   | 匹配前一个字符1次或无限次                                                        |
|   `?`   | 匹配前一个字符0次或1次                                                           |
|  `{m}`  | 匹配前一个字符m次                                                                |
| `{m,n}` | 匹配前一个字符m至n次。 m和n可以省略: 省略m表示匹配0到n次；省略n表示匹配m至无限次 |

``` python
# re_repetition.py

from re_text_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('ab*', 'a followed by zero or more b'),
     ('ab+', 'a followed by one or more b'),
     ('ab?', 'a followed by zero or one b'),
     ('ab{3}', 'a followed by three b'),
     ('ab{2,3}', 'a followed by two to three b')],
)
```

匹配到 `ab*`和`ab?`的比 `ab+`多：

    $ python3 re_repetition.py

    'ab*' (a followed by zero or more b)

      'abbaabbba'
      'abb'
      ...'a'
      ....'abbb'
      ........'a'

    'ab+' (a followed by one or more b)

      'abbaabbba'
      'abb'
      ....'abbb'

    'ab?' (a followed by zero or one b)

      'abbaabbba'
      'ab'
      ...'a'
      ....'ab'
      ........'a'

    'ab{3}' (a followed by three b)

      'abbaabbba'
      ....'abbb'

    'ab{2,3}' (a followed by two to three b)

      'abbaabbba'
      'abb'
      ....'abbb'

当处理一个重复的匹配模式时，`re` 总是尽可能的匹配到多的子字符串，称为贪婪模式。
贪婪模式可能会导致更少的单独匹配以及与预期不相符的匹配过多。通过在正则表达式后面加上一个
`?` 就可以切换到非贪婪模式。

``` python
# re_repetition_non_greedy.py

from re_text_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('ab*?', 'a followed by zero or more b'),
     ('ab+?', 'a followed by one or more b'),
     ('ab??', 'a followed by zero or one b'),
     ('ab{3}?', 'a followed by three b'),
     ('ab{2,3}?', 'a followed by two to three b')],
)
```

非贪婪模式下，正则表达式便会尽可能的少匹配重复的字符。

    $ python3 re_repetition_non_greedy.py

    'ab*?' (a followed by zero or more b)

      'abbaabbba'
      'a'
      ...'a'
      ....'a'
      ........'a'

    'ab+?' (a followed by one or more b)

      'abbaabbba'
      'ab'
      ....'ab'

    'ab??' (a followed by zero or one b)

      'abbaabbba'
      'a'
      ...'a'
      ....'a'
      ........'a'

    'ab{3}?' (a followed by three b)

      'abbaabbba'
      ....'abbb'

    'ab{2,3}?' (a followed by two to three b)

      'abbaabbba'
      'abb'
      ....'abb'

## 字符集

字符集是指一组字符，匹配的可以是字符集中的任一字符。例如，`[ab]` 可以匹配`a`或者`b`。

``` python
# re_charset.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('[ab]', 'either a or b'),
     ('a[ab]+', 'a followed by 1 or more a or b'),
     ('a[ab]+?', 'a followed by 1 or more a or b, not greedy')],
)
```

`a[ab]+` 匹配到了整个字符串，在贪婪模式下，字符`a`后都是`a`或者`b`。

    $ python3 re_charset.py

    '[ab]' (either a or b)

      'abbaabbba'
      'a'
      .'b'
          ..'b'
      ...'a'
      ....'a'
      .....'b'
      ......'b'
      .......'b'
      ........'a'

    'a[ab]+' (a followed by 1 or more a or b)

      'abbaabbba'
      'abbaabbba'

    'a[ab]+?' (a followed by 1 or more a or b, not greedy)

      'abbaabbba'
      'ab'
      ...'aa'

一个字符集也可以用来排除特定的字符，`^` 表示匹配字符集中以外的字符。

``` python
# re_charset_exclude.py
from re_test_patterns import test_patterns

test_patterns(
    'This is some text -- with punctuation.',
    [('[^-. ]+', 'sequences without -, ., or space')],
)
```

这个正则表达式pattern匹配了所有除了`-`， `.`和空格以外的字符。


    $ python3 re_charset_exclude.py

    '[^-. ]+' (sequences without -, ., or space)

      'This is some text -- with punctuation.'
      'This'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'

如果需要匹配的字符集数目较多，每个都打出来费时费力。更为紧凑的字符集格式是利用`-`链接开始字符和结束字符，表示范围内的所有字符。

``` python
# re_charset_ranges.py
from re_test_patterns import test_patterns

test_patterns(
    'This is some text -- with punctuation.',
    [('[a-z]+', 'sequences of lowercase letters'),
     ('[A-Z]+', 'sequences of uppercase letters'),
     ('[a-zA-Z]+', 'sequences of letters of either case'),
     ('[A-Z][a-z]+', 'one uppercase followed by lowercase')],
)
```

范围 `a-z` 包括小写的ASCII字符，`A-Z` 包括所有的大写 ASCII 字符。 两个范围也可以合并为
一个字符集 `[a-zA-z]`.

    $ python3 re_charset_ranges.py

    '[a-z]+' (sequences of lowercase letters)

      'This is some text -- with punctuation.'
      .'his'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'

    '[A-Z]+' (sequences of uppercase letters)

      'This is some text -- with punctuation.'
      'T'

    '[a-zA-Z]+' (sequences of letters of either case)

      'This is some text -- with punctuation.'
      'This'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'

    '[A-Z][a-z]+' (one uppercase followed by lowercase)

      'This is some text -- with punctuation.'
      'This'

作为字符集的特殊情况，元字符 点: `.` 可以匹配任何单个字符。

``` python
# re_charset_dot.py
from re_test_patterns import test_patterns

test_patterns(
    'abbaabbba',
    [('a.', 'a followed by any one character'),
     ('b.', 'b followed by any one character'),
     ('a.*b', 'a followed by anything, ending in b'),
     ('a.*?b', 'a followed by anything, ending in b')],
)
```
将 `.` 与重复字符组合可以匹配很长的字符，除非用非贪婪模式。

    $ python3 re_charset_dot.py

    'a.' (a followed by any one character)

      'abbaabbba'
      'ab'
      ...'aa'

    'b.' (b followed by any one character)

      'abbaabbba'
      .'bb'
      .....'bb'
      .......'ba'

    'a.*b' (a followed by anything, ending in b)

      'abbaabbba'
      'abbaabbb'

    'a.*?b' (a followed by anything, ending in b)

      'abbaabbba'
      'ab'
      ...'aab'

## 转义字符


