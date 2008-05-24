Testing roadrunner
==================

First off let's create a sample test for roadrunner to run

>>> from roadrunner.tests.fixtures import copy_test_packages
>>> copy_test_packages(buildout_directory)
>>> write('buildout.cfg', """\
[buildout]
parts=roadrunner
develop=
  test/testpackages/test-preloaded-package
  test/testpackages/test-preloaded-package

[roadrunner]
recipe = roadrunner
preload-packages =
  test-preloaded-package
package-under-test =
  test-package
""")
>>> 

Other options to speed up Plone testing
=======================================

plone.reload / ReloadNG:

- These two rely on Guido's xreload module which was introduced sometime last year.

- It needs a lot of hacks to make it work. By comparison, roadrunner forks a
  process. That's the only trick. The numbers of lines of code could be even
  simpler if it was better integrated into the zope testrunner somehow.
  
TODO
====

- ability to preload any arbitrary layers, plus some presets like --plone or --grok.
This could be done via 

- hooks for fixture configuration?
- tests... how ironic this code has none, but it started as a proof of concept
- prevent layer destruction for an added half second

