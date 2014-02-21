
@property
def jeejee():
  print("in jeejee()")
  return "ROCK"

print(jeejee)

# VS

class A:
  
  @property
  def jeejee(self):
    print("in jeejee()")
    return "ROCK"

a = A()
print(a.jeejee)