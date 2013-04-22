# -*- coding: utf-8 -*-
# rest reader from pelican , rstdirectives also included 

import docutils.core
import docutils.io
from docutils.writers.html4css1 import HTMLTranslator
from docutils import nodes, utils
from docutils.parsers.rst import directives, roles, Directive
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
import re
import datetime
import logging
log = logging.getLogger(__name__)
import os

class _Translator(HTMLTranslator):

    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr('explanation'):
            attrs['title'] = node['explanation']
        self.body.append(self.starttag(node, 'abbr', '', **attrs))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

def _field_date(name,value):
  return datetime.datetime.strptime(value,"%Y-%m-%d")

def _field_tags(name,value):
  return set(value.strip().split())

def _field_default(name,value):
  log.debug("Unknown field {}".format(name))
  return value

def _get_docinfo(document):
  """Return the dict containing document metadata"""
  output = {}
  for docinfo in document.traverse(docutils.nodes.docinfo):
    for element in docinfo.children:
      if element.tagname == 'field':  # custom fields (e.g. summary)
        name_elem, body_elem = element.children
        name = name_elem.astext()
        value = body_elem.astext()
      else:  # standard fields (e.g. address)
        name = element.tagname
        value = element.astext()
      name = name.lower()
      value = globals().get("_field_" + name,_field_default)(name,value)
      output[name] = value 
  return output

def _get_files(document, manager):
  result = list()
  for image in document.traverse(docutils.nodes.image):
    log.debug(image)
    #image["uri"] = manager.ext_file(image.get("uri"))
    manager.ext_file(image.get("uri"))
  return result

def _get_publisher(source_path):
  extra_params = {'initial_header_level': '2',
                  'syntax_highlight': 'short',
                  "output_encoding": 'utf-8'}
  pub = docutils.core.Publisher(destination_class=docutils.io.StringOutput)
  pub.set_components('standalone', 'restructuredtext', 'html')
  pub.writer.translator_class = _Translator
  pub.process_programmatic_settings(None, extra_params, None)
  pub.set_source(source_path=source_path)
  pub.publish()
  return pub

def path_to_title(path):
  return os.path.basename(os.path.splitext(path)[0]) \
           .replace("-"," ").replace("_"," ").capitalize()

def read(source_path, manager):
  """ Get data from rest file.
  Returns content as str, info as dict.
  """
  pub = _get_publisher(source_path)
  parts = pub.writer.parts
  content = parts.get('body')
  info = _get_docinfo(pub.document)
  ## fix missing required fields
  info.setdefault("title", parts.get('title'))
  if info["title"].strip() == "":
    info["title"] = path_to_title(source_path)
  info.setdefault("date", datetime.datetime.fromtimestamp(
    os.path.getmtime(source_path)))
  info.setdefault("tags", set())
  ##
  _get_files(pub.document, manager)
  ##
  return content, info

INLINESTYLES = False
DEFAULT = HtmlFormatter(noclasses=INLINESTYLES)
VARIANTS = {
    'linenos': HtmlFormatter(noclasses=INLINESTYLES, linenos=True),
}

class Pygments(Directive):
    """ Source code syntax hightlighting.
    """
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict([(key, directives.flag) for key in VARIANTS])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()
        # take an arbitrary option if more than one is given
        formatter = self.options and VARIANTS[self.options.keys()[0]] \
                    or DEFAULT
        parsed = highlight('\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

directives.register_directive('code', Pygments)

class YouTube(Directive):
    """ Embed YouTube video in posts.

    Courtesy of Brian Hsu: https://gist.github.com/1422773

    VIDEO_ID is required, with / height are optional integer,
    and align could be left / center / right.

    Usage:
    .. youtube:: VIDEO_ID
        :width: 640
        :height: 480
        :align: center
    """

    def align(argument):
        """Conversion function for the "align" option."""
        return directives.choice(argument, ('left', 'center', 'right'))

    required_arguments = 1
    optional_arguments = 2
    option_spec = {
        'width': directives.positive_int,
        'height': directives.positive_int,
        'align': align
    }

    final_argument_whitespace = False
    has_content = False

    def run(self):
        videoID = self.arguments[0].strip()
        width = 420
        height = 315
        align = 'left'

        if 'width' in self.options:
            width = self.options['width']

        if 'height' in self.options:
            height = self.options['height']

        if 'align' in self.options:
            align = self.options['align']

        url = 'http://www.youtube.com/embed/%s' % videoID
        div_block = '<div class="youtube" align="%s">' % align
        embed_block = '<iframe width="%s" height="%s" src="%s" '\
                      'frameborder="0"></iframe>' % (width, height, url)

        return [
            nodes.raw('', div_block, format='html'),
            nodes.raw('', embed_block, format='html'),
            nodes.raw('', '</div>', format='html')]

directives.register_directive('youtube', YouTube)

_abbr_re = re.compile('\((.*)\)$')


class abbreviation(nodes.Inline, nodes.TextElement):
    pass


def abbr_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    m = _abbr_re.search(text)
    if m is None:
        return [abbreviation(text, text)], []
    abbr = text[:m.start()].strip()
    expl = m.group(1)
    return [abbreviation(abbr, abbr, explanation=expl)], []

roles.register_local_role('abbr', abbr_role)

if __name__ == "__main__":
  print(read("/home/hevi/wrk/blog/creating-static-blog-generator.rst"))
