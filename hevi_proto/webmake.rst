WebMake
*******

Ability to run a make or other "build" commands from browser and
get build results into page.

Motivation
==========

Presentation and management of build output text.

Use
===

Start local process webappserver in current build directory::

  /wrk/project> webmake.py
  
which open browser and runs make and redirects make stdout and stderr
into web page text.

Related
=======

CI (Continuous Integration) frameworks.

Challenges
==========

ansi terminal code formatting of the output text.

recursive submakes ?

Continuous output and web-frameworks and html page structure. Producing
the make output content may take 30mins but page structure needs end
html tags immediately.   