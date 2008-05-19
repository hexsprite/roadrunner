roadrunner
++++++++++

aka. looping testrunner with environment preloading for test-driven development

preloads a standard Zope & Plone test environment compatible with
PloneTestCase.

Tests are then run in a loop.  You are given a shell-like environment with
command history where you can select different tests, etc.

Limitations
===========

Because it preloads the Plone environment you won't be able to see changes
to the Core Plone components.  However, it should see all changes in your
application code which is what you will most likely be changing anyways.

Currently you may need to remove any modules under test from the zcml line in
your [instance] section so that it will only initialize your test environment.

If you follow normal testing conventions you will be loading your ZCML
as a layer setup deferred anyways.

Theoretically this should be able to work with any test environment (eg. 
Django, TG, Twisted).

I eventually plan to do this, and would accept any patches in the meantime
if anyone feels so inclined.

How to use it?
==============

Roadrunner only currently works as part of a buildout.

Easiest way to try it is to add it to an existing Plone 3 buildout.

Here's a sample part::

  [roadrunner]    
  recipe = zc.recipe.egg
  eggs =
      ${instance:eggs}
      roadrunner
  extra-paths = ${instance:zope2-location}/lib/python
  initialization =
      conf_file = "${instance:location}/etc/zope.conf"
  arguments = conf_file, "${instance:zope2-location}", "${buildout:directory}"

Yes it's ugly.  It will get fixed eventually.

Then you can run roadrunner::

  $ bin/roadrunner -s Products.PasswordResetTool

Author
======

Jordan Baker <jbb@scryent.com>