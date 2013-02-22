

"""
State Machine
=============

class Sample:
  
  states = STATE("INIT","CONN","READY")
  
  states = (
    STATE(      "INIT","CONN","READY")
    IN("input1","CONN"  )
  )
  
  jj = {
    input1: ("CONN",)
  }
"""