Testing roadrunner
==================

Warning for those who would run this buildout it is an insane test. In order
to properly test things we build and run Plone.  For developing on roadrunner
you could re-use an existing Zope & Plone install to speed things up.

First off let's create a sample buildout for roadrunner to run

  >>> import os
  >>> write(sample_buildout, 'buildout.cfg', plone_buildout_cfg)

We'll want to restore the default PYPI index to find required Plone packages
for this test.  Yes its a bit of a heavy integration test.
  
  >>> import zc.buildout.easy_install
  >>> import os
  >>> zc.buildout.easy_install.default_index_url = 'http://cheeseshop.python.org/pypi'
  >>> os.environ['buildout-testing-index-url'] = (
  ...   zc.buildout.easy_install.default_index_url)
  
Setup a preloaded package. This is a package that should be preloaded. We
don't need to see the changes in this module without restarting the testrunner.

  >>> mkdir(sample_buildout, 'src')
  >>> mkdir(sample_buildout, 'src', 'test_package')
  >>> write(sample_buildout, 'src', 'test_package', '__init__.py', '#')
  >>> write(sample_buildout, 'src', 'test_package', 'setup.py',
  ... """
  ... from setuptools import setup
  ...
  ... setup(
  ...     name = "test_package",
  ...     )
  ... """)
  >>> write(sample_buildout, 'src', 'test_package', 'tests.py', 
  ... """
  ... from test_package.mymod import changed_value
  ...
  ... class TestSetup:
  ...   def test_value(self):
  ...     self.failIf(changed_value)
  ... def test_suite():
  ...   return unittest.TestSuite((
  ...     unittest.makeSuite(TestSetup),
  ...   ))
  ...
  ... if __name__ == '__main__':
  ...   unittest.main(defaultTest='test_suite')
  ... """)
  >>> write(sample_buildout, 'src', 'test_package', 'mymod.py',
  ... """
  ... changed_value=False
  ... """)
  
Setup a package under test.  This would be a package you would be developing
and wanted to see any changes that were made as you were testing.

  >>> mkdir(sample_buildout, 'src', 'preloaded_package')
  >>> write(sample_buildout, 'src', 'preloaded_package', 'setup.py',
  ... """
  ... from setuptools import setup
  ...
  ... setup(
  ...     name = "preloaded_package",
  ...     )
  ... """)
  >>> mkdir(sample_buildout, 'src', 'preloaded_package')
  >>> write(sample_buildout, 'src', 'preloaded_package', '__init__.py', '#')
  >>> write(sample_buildout, 'src', 'preloaded_package', 'tests.py', 
  ... """
  ... from preloaded_package.mymod import changed_value
  ...
  ... class TestSetup:
  ...   def test_value(self):
  ...     self.failIf(changed_value)
  ... def test_suite():
  ...   return unittest.TestSuite((
  ...     unittest.makeSuite(TestSetup),
  ...   ))
  ...
  ... if __name__ == '__main__':
  ...   unittest.main(defaultTest='test_suite')
  ... """)
  >>> write(sample_buildout, 'src', 'preloaded_package', 'mymod.py',
  ... """
  ... changed_value=False
  ... """)
  
Run the buildout:

  >>> buildout = os.path.join('bin', 'buildout')
  >>> print system(buildout + " -N") # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
  Develop: '/sample-buildout/src/test_package'
  Develop: '/sample-buildout/src/preloaded_package'
  Develop: '/Users/jbb/co/myplatform_buildout/trunk/src/roadrunner/roadrunner/..'
  Installing plone.
  Not found: None
  Installing instance.
  Generated script '/sample-buildout/bin/instance'.
  Generated script '/sample-buildout/bin/repozo'.
  Installing roadrunner.
  Generated script '/sample-buildout/bin/rrplone'.
  Unused options for roadrunner: 'package-under-test'.
  <BLANKLINE>
  
Run roadrunner and talk to it via pexpect module.

  >>> import pexpect
  >>> rr = pexpect.spawn("bin/rrplone -s test_package")
  >>> rr.timeout = 30
  >>> rr.logfile = file("/tmp/rr.log", 'w')
  >>> success_test_pattern = "0 failures"
  >>> fail_test_pattern = "1 failures"
  >>> import pdb; pdb.set_trace()
  >>> rr.expect(success_test_pattern)
  >>> rr.expect('rr>')

Now I change something in the package under test.  it should show up in the test runner.

  >>> write('src', 'test_package', 'test_package', 'mymod.py', "changed_value = True")

Re-run the test and check for a failed result now

  >>> rr.sendline("test -s test_package")
  >>> rr.expect(fail_test_pattern)
  >>> rr.expect('rr>')

Run the preloaded package.

  >>> rr.sendline("test -s preloaded_package")
  >>> rr.expect(success_test_pattern)
  >>> rr.expect('rr>')

Make a change in the preloaded package.  It won't show up.

  >>> rr.sendline("test -s preloaded_package")
  >>> rr.expect(success_test_pattern)
  >>> rr.expect('rr>')

Quit the runner

  >>> rr.sendline("exit")
  >>> rr.kill()
  
TODO: is that it to close?

