

class A:
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name
    

a = A("test")

#a.name = "no"
del a.name
