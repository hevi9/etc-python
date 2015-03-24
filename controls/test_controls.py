

from controls8 import _Base

def test_Base_path():
  root = _Base()
  sub1 = _Base(root, "sub1")
  sub2 = _Base(sub1, "sub2")
  assert sub2.path == "sub1.sub2"
