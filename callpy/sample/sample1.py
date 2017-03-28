
def samplerun1():
    print("samplerun1")

class CallClass:

    def __call__(self, *args, **kwargs):
        print("CallClass", args)

sampleclass1 = CallClass()