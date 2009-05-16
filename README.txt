Waiting for stuff sucks.

roadrunner is a resident looping test runner optimized for rapid test development.

Currently it is focused around preloading a Plone environment but it could
also work for other frameworks as well.

It works by pre-loading Python code, setup of test layers and a default Plone
site. This is called the resident test environment.

Your tests are run in a child process which gets a copy-on-write memory space.

Other than that it pretty much works like the regular Zope testrunner.

How much faster is it?
======================

Here's an example. You are writing integration or functional tests for a Plone
application.

On this fairly current laptop it takes 25s to load Zope, Plone and setup a
sample Plone site.

Add 5 seconds for the application load and test run for a total of 30 seconds.

If you are iterating on a functional test and want to quickly check your
changes that is too long to wait.

Using roadrunner you load the environment the first time.  Subsequent times
you run your test your total time will be only 5 seconds.

Yes, you can save 25 seconds every time you run your test.

How to use it?
==============

Roadrunner only currently works as part of a zc.buildout environment.

The easiest way to try it is to add it to an existing Plone 3 buildout.

Now for a sample part.

This will create a new directory in parts named by the part containing a copy
of your Zope instance environment but with the packages-under-test excluded
from being loaded via ZCML by default.

::

  [roadrunner]
  recipe = roadrunner:plone
  packages-under-test = my.package
  
You can also match several packages using simple globbing, eg: my.packages.*

The parameter 'zope2-instance' allows you to specify the name of the part
which corresponds to the zope instance roadrunner will work against.  The
default is 'instance'.

By default resident Plone site will be created. This should work in most
situations where you are installing add-on products that use install methods
or GenericSetup profiles.

setup-plone=0 allows you to disable the Plone site setup optimization. You
might need to do this in certain situations where you are using the profile_id
parameter.

Then you can run roadrunner::

  $ bin/roadrunner -s my.package
  
It will preload Zope & Plone, then fork off the first testrunner. Once the
first testrunner is complete you will receive the roadrunner prompt where
you launch additional tests.

Gotchas
=======

- roadrunner is still a bit experimental. If in doubt, check it with the
  regular testrunner. If you find a difference please send some details
  including traceback, product versions, buildout.cfg and your tests.

- It may require you to change your test setup slightly if you haven't yet
  already.

  You'll be fine as long as you follow the standard sequence of importing your
  product, loading its ZCML and then calling ztc.installProduct within an
  @onsetup deferred method.
  
   This allows the loading of your product to occur in the child testrunner
  process which critical that roadrunner does what its supposed to do.

  For more details see an example here:

    http://plone.org/documentation/tutorial/testing/writing-a-plonetestcase-unit-integration-test
  
- Because it preloads the Plone environment you won't be able to see changes
  to the Core Plone components.  However, it should see all changes in your
  application code which is what you will most likely be changing anyways.
  
  This is being worked on.

Other options to speed up Plone testing
=======================================


- plone.reload, which relies on Guido's xreload module and some extra patches
  to work with Zope. Works quite well for TTW software testing and
  development. In future releases I may find a way to incorporate it into
  roadrunner.

Tested With
===========

Plone 3.1. Let me know if you get it working on anything else.

Also there are reports of success with Zope 2.9.8 and Plone 2.5.5.

Windows is untested and probably does not work currently. Feedback and patches
accepted.

Author
======

Send questions, comments & bug reports to:

Jordan Baker <jbb@no_spam_plz_scryent.com>

License
=======

Licensed under ZPL 2.1
see doc/LICENSE.txt
