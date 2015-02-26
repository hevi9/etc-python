
# http://reinout.vanrees.org/weblog/2010/01/06/zest-releaser-entry-points.html

from setuptools import setup

name = "setuptoolsx"


setup(
  name=name,
  entry_points = {
    "console_scripts": [
      "setuptoolsx = testplugin:main"
    ],
    name: [
      "testplugin = testplugin:entry",
      "testplugin2 = testplugin:entry"
    ]
  }
)
