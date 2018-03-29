
class A:

    def op(self):
        print("op")
        return self


def fn():
    a = ( A() 
        .op() )



fn()

