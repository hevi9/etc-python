import io # http://docs.python.org/3/library/io.html
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser
from docutils.io import StringInput
from docutils.frontend import OptionParser
from docutils.utils import new_document
from docutils.writers.html4css1 import Writer
import sys

text = """

Title
#####

"""

def get_settings():
  settings = OptionParser().get_default_values()
  ## parser settings
  settings.tab_width = 2
  settings.pep_references = None
  settings.rfc_references = None
  ## html settinfgs
  settings.xml_declaration = None
  settings.stylesheet = None
  settings.stylesheet_path = None
  settings.initial_header_level = 1
  settings.math_output = "X"
  settings.template = Writer.default_template_path
  return settings


def read1(text):
  reader = Reader()
  source = StringInput(text)
  parser = Parser() # one time
  document = reader.read(source, parser, get_settings())
  return document
  
def read2(text):
  parser = Parser()
  source_path = "<string>"
  document = new_document(source_path, get_settings())
  parser.parse(text, document)
  return document
  
def translate_to_parts(document):
  writer = Writer()
  writer.document = document
  writer.translate()
  writer.assemble_parts()
  return dict(writer.parts)
  
#print(read1(text))
#print(read2(text))

print(translate_to_parts(read2(text)))

