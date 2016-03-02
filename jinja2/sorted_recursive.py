class Node:

    def __init__(self, name, *subs):
        self.name = name
        self.subs = set(subs)


root = Node("A",
            Node("B4",
                 Node("C2",
                      Node("D3"),
                      Node("D1"),
                      Node("D2")
                      ),
                 Node("C1")
                 ),
            Node("B2"),
            Node("B1",
                 Node("C4"),
                 Node("C3"),
                 Node("C2"),
                 Node("C1")
                 ),
            Node("B3")
            )

print("*** reference")


def walk(node):  # reference
    print(node.name)
    for i in sorted(node.subs, key=lambda x: x.name):
        walk(i)
walk(root)

print("*** jinja2")
from jinja2 import Template

tmpl = Template("""
{{ root.name }}
{%- for node in root.subs | sort(attribute='name') recursive %}
{{ node.name }}
{%- if node.subs %}{{ loop(node.subs | sort(attribute='name')) }}{%- endif %}
{%- endfor %}
""")

print(tmpl.render(root=root))
