roadrunner
++++++++++

because waiting for stuff sucks

- A looping testrunner with environment preloading for test-driven
  development.

- Preloads a standard Zope & Plone test environment compatible with
  PloneTestCase.

- Tests are then run in a loop. You are given a shell-like environment with
  command history where you can select different tests, etc.
  
How to use it?
==============

Roadrunner only currently works as part of a zc.buildout environment.

The easiest way to try it is to add it to an existing Plone 3 buildout.

Here's a sample part::

  [roadrunner]
  recipe = roadrunner:plone
  packages-under-test = my.package.*

This will create a new directory in parts named by the part containing a copy
of your Zope instance environment.

Then you can run roadrunner::

  $ bin/roadrunner -s my.package 

Limitations
===========

- roadrunner is still a bit experimental. I haven't yet seen a situation where
  it did not work as planned, but it may expose if your test setup does things
  out of order.

  You'll be fine as long as you follow the standard sequence of importing your
  product, loading its ZCML and then calling ztc.installProduct within an
  @onsetup deferred method.

  For more details see an example here:

    http://plone.org/documentation/tutorial/testing/writing-a-plonetestcase-unit-integration-test
  
- Because it preloads the Plone environment you won't be able to see changes
  to the Core Plone components.  However, it should see all changes in your
  application code which is what you will most likely be changing anyways.
  
- Theoretically this should be able to work with any test environment (eg.
  Django, TG, Twisted).

  I eventually plan to do this, and would accept any patches in the meantime
  if anyone feels so inclined.

Other options to speed up Plone testing
=======================================

plone.reload / ReloadNG:

- These two rely on Guido's xreload module.

- It needs a lot of hacks to make it work because of complicated bits in
  Zope2. roadrunner by comparison just gives up trying to hack Zope2 and
  relies on a process checkpoint method.  I'm still trying to figure out
  if plone.reload could help roadrunner and vice versa.
  
Tested With
===========

Plone 3.1. Let me know if you get it working on anything else.

Author
======

Send questions, comments & bug reports to:

Jordan Baker <jbb@scryent.com>

License
=======
Licensed under ZPL 2.1
see doc/LICENSE.txt
