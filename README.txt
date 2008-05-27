Waiting for stuff sucks.

roadrunner is a looping testrunner with environment preloading for test-driven
development.

It preloads a standard Zope & Plone test environment compatible with
PloneTestCase. After the first load of the test environment I have been 
saving around 25s per test run on my Macbook Pro 2.16.

Other than that it pretty much works like the regular Zope testrunner.

How to use it?
==============

Roadrunner only currently works as part of a zc.buildout environment.

The easiest way to try it is to add it to an existing Plone 3 buildout.

Here's a sample part::

  [roadrunner]
  recipe = roadrunner:plone
  packages-under-test = my.package

You can also match several packages using simple globbing, eg: my.packages.*

This will create a new directory in parts named by the part containing a copy
of your Zope instance environment but with the packages-under-test excluded
from being loaded via ZCML by default.

Then you can run roadrunner::

  $ bin/roadrunner -s my.package
  
It will preload Zope & Plone, then fork off the first testrunner. Once the
first testrunner is complete you will receive the roadrunner prompt where
you launch additional tests.

Gotchas
=======

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

Jordan Baker <jbb@no_spam_plz_scryent.com>

License
=======
Licensed under ZPL 2.1
see doc/LICENSE.txt
