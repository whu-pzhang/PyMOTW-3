# textwrap

`textwrap`模块用来格式化输入来获得好看的打印效果。


```python
sample_text = """
    The textwrap module can be used for format text for output in
    situations where pretty-printing is desired. It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
"""
```

## 段落填充

`fill()`函数可以输出格式化的文本


```python
# textwrap_fill.py

import textwrap

print(textwrap.fill(sample_text, width=50))
```

         The textwrap module can be used for format
    text for output in     situations where pretty-
    printing is desired. It offers     programmatic
    functionality similar to the paragraph wrapping
    or filling features found in many text editors.


首行缩进，余下行左对齐


```python
import textwrap

text = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

print(textwrap.fill(text, width=50, initial_indent="  ", subsequent_indent="    "))
```

      Look into my eyes, look into my eyes, the eyes,
        the eyes, the eyes, not around the eyes, don't
        look around the eyes, look into my eyes,
        you're under.


同时可以指定第一行和余下行的缩进大小。

## 移除缩进



```python
import textwrap

dedented_text = textwrap.dedent(sample_text)
print('Dedented:')
print(dedented_text)
```

    Dedented:
    
    The textwrap module can be used for format text for output in
    situations where pretty-printing is desired. It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    


`dedent`是缩进(`indent`)的反义词，会移除文本的公共缩进空白部分，文本内的相对缩进则不会移除。


```python
text = """
 Line one.
     Line two.
 Line three.
"""

import textwrap
print("Original:")
print(text)
print("Dedent:")
print(textwrap.dedent(text))
```

    Original:
    
     Line one.
         Line two.
     Line three.
    
    Dedent:
    
    Line one.
        Line two.
    Line three.
    


## 填充和反缩进联合使用


```python
# textwrap_fill_width.py

import textwrap

dedent_text = textwrap.dedent(sample_text).strip()
for width in {45, 60}:
    print("{} Colums:\n".format(width).strip())
    print(textwrap.fill(dedent_text, width=width))
    print()
```

    60 Colums:
    The textwrap module can be used for format text for output
    in situations where pretty-printing is desired. It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    
    45 Colums:
    The textwrap module can be used for format
    text for output in situations where pretty-
    printing is desired. It offers programmatic
    functionality similar to the paragraph
    wrapping or filling features found in many
    text editors.
    


输出为固定宽度的段落

## 块缩进

`indent()`函数可以对文本所有行加上统一的前缀。下面的例子将文本格式化为邮件引文的形式


```python
# textwrap_indent.py

import textwrap

dedent_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedent_text, width=50)
wrapped += "\n\nSecond paragraph after a blank line."
final = textwrap.indent(wrapped, '>')

print("Quoted block:\n")
print(final)
```

    Quoted block:
    
    > The textwrap module can be used for format text
    >for output in situations where pretty-printing is
    >desired. It offers programmatic functionality
    >similar to the paragraph wrapping or filling
    >features found in many text editors.
    
    >Second paragraph after a blank line.



```python

```
