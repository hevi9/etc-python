
text = """
sample text.
  test

1. test tes

 1.2  test
  
"""

space = set(" \n\t")

def textract(text):
  for ch in text:
    if ch in space:
      print("SP", ord(ch))
    else:
      print("CH", ch)

textract(text)

