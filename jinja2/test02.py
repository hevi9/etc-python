from jinja import Environment
env = Environment()
tmpl = env.from_string('Hello {{ name }}!')
print tmpl.render(name='John Doe')

