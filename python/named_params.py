

def func(*,section="default",name="default name"):
  print("func",section,name)
  
func()

func(name="testing", section="joo joo")


def func2(*,section,name):
  print("func",section,name)

func2(name="2 testing", section="2 joo joo")

#func2(section="2 joo joo")

def func3(*, section: str = None, id: int, thing="any"):
  print("func",section,id)
  print(func3.__annotations__)

func3(id=123, section="2 joo joo")
