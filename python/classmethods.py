
##############################################################################

def getLevelName(arg):
  return arg

def addLevelName(arg):
  return arg

getLevelName(111)

addLevelName(111)

##############################################################################

def LevelName_get(arg):
  return arg

def LevelName_add(arg):
  return arg

LevelName_get(111)

LevelName_add(111)

#############################################################################

class LevelName:

  @classmethod
  def get(cls,arg):
    return arg
  
  @classmethod
  def add(cls,arg):
    return arg
  
LevelName.get(111)
LevelName.add(111)
  
#############################################################################

class LevelName2:

  def get(cls,arg):
    return arg
  
  def add(cls,arg):
    return arg
  
l = LevelName()
l.get(111)
l.add(111)
  
#############################################################################