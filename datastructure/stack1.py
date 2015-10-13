
class Stack(list):

    push = list.append

    def __call__(self):
        return self[-1]


s = Stack()
print(repr(s), bool(s))

s.push(1)
print(repr(s), bool(s))

s.pop()
print(repr(s), bool(s))

s.push(2)
print(repr(s), bool(s), s())

s.pop()

s.push(1)
s.push(2)
s.push(3)
print(repr(s), bool(s), s())