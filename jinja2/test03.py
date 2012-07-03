from jinja import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))
tmpl = env.get_template('test03_index.html')
d = { 'John Doe' : 1, "juu ei" : 2, "Joo o" : 3}
print tmpl.render(names=d)
