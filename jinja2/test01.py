from jinja import from_string
print from_string('Hello {{ data }}!').render(data='World')

