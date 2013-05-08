import io # http://docs.python.org/3/library/io.html
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser
from docutils.io import StringInput
from docutils.frontend import OptionParser

text = """

Title
#####

"""

reader = Reader()
source = StringInput(text)
parser = Parser() # one time
settings = OptionParser().get_default_values()
settings.tab_width = 2
settings.pep_references = None
settings.rfc_references = None
document = reader.read(source, parser, settings)
print(document)

"""

1. Create a parser::

       parser = docutils.parsers.rst.Parser()

   Several optional arguments may be passed to modify the parser's behavior.
   Please see `Customizing the Parser`_ below for details.

2. Gather input (a multi-line string), by reading a file or the standard
   input::

       input = sys.stdin.read()

3. Create a new empty `docutils.nodes.document` tree::

       document = docutils.utils.new_document(source, settings)

   See `docutils.utils.new_document()` for parameter details.

4. Run the parser, populating the document tree::

       parser.parse(input, document)

"""