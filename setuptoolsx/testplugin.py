from pkg_resources import iter_entry_points

group = "setuptoolsx"

def entry():
  print("ENTRY HERE")
  
class entry:
  
  def get_wsgi():
    print("get_wsgi")
    
  def get_tmpl():
    print("get_tmpl")
  
def main():
  print("MAIN HERE")
  for entry_point in iter_entry_points(group=group):
    print("Loading", entry_point.name)
    print("attrs", entry_point.attrs)
    entry = entry_point.load()
    entry.get_wsgi()
    entry.get_tmpl()
 
print("ON LOAD")