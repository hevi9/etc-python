import regex as re


pattern = r'(?P<empty>^[ \t]*$)|(?P<nl>$)'
pattern = r'(?P<empty>^[ \t]*\n)|(?P<nl>\n)'
pattern = r'(?P<nl>(?!^[ \t]*)\n)|(?P<empty>^[ \t]*\n)'

pattern2 = r'(?P<nl>\n)|(?P<empty>^[ \t]*$)'

reo = re.compile(pattern, re.MULTILINE)


text = """
x

y  
"""

for mo in reo.finditer(text, overlapped=True):
    print(mo, mo.lastgroup)