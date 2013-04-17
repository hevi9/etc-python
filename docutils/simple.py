"""
http://svn.plone.org/svn/collective/collective.checkdocs/trunk/collective/checkdocs/__init__.py
"""

from docutils.core import publish_parts

def rst2html(value):
    """ Run rst2html translation """
    docutils_settings = {}
    parts = publish_parts(source=value,
            writer_name="html4css1",
            settings_overrides=docutils_settings)
    return parts['whole']

def rst2html2(value):
    """ Run rst2html translation """
    docutils_settings = {}
    parts = publish_parts(source=value,
            writer_name="html4css1",
            settings_overrides=docutils_settings)
    return parts['body']

def rst2html3(value):
    """ Run rst2html translation """
    docutils_settings = {}
    parts = publish_parts(source=value,
            writer_name="html4css1",
            settings_overrides=docutils_settings)
    return parts['docinfo']

def rst2html4(value):
    """ Run rst2html translation """
    docutils_settings = {}
    parts = publish_parts(source=value,
            writer_name="html4css1",
            settings_overrides=docutils_settings)
    return parts['title']
  
text = """
Testing
#######
:date: 1990
:tags: joo jee

lskaj klas 
asldal djlk:

* lkasddjakl

* sadljdasl

askldasj

:nohere: jee

"""  

print(rst2html4(text))
