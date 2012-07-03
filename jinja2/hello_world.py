from jinja2 import Template
print(Template('Hello {{ data }}!').render(data='World'))

