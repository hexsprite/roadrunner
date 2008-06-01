import os, re, shutil, sys
import zc.buildout.tests
import zc.buildout.testing

import unittest
from zope.testing import doctest, renormalizing

os_path_sep = os.path.sep
if os_path_sep == '\\':
    os_path_sep *= 2

def dirname(d, level=1):
    if level == 0:
        return d
    return dirname(os.path.dirname(d), level-1)

def setUp(test):
    zc.buildout.tests.easy_install_SetUp(test)
    
def test_suite():
    globs = dict(plone_buildout_cfg=plone_buildout_cfg)
    suite = unittest.TestSuite((
        doctest.DocFileSuite(
            'recipe.txt',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            globs=globs,
            checker=renormalizing.RENormalizing([
               zc.buildout.testing.normalize_path,
               zc.buildout.testing.normalize_script,
               zc.buildout.testing.normalize_egg_py,
               zc.buildout.tests.normalize_bang,
               (re.compile('zc.buildout(-\S+)?[.]egg(-link)?'),
                'roadrunner'),
               (re.compile('[-d]  setuptools-[^-]+-'), 'setuptools-X-')
               ]),
            # optionflags=doctest.ABORT_AFTER_FIRST_FAILURE,
            ),
        ))
    
    return suite
    
plone_buildout_cfg = """\
[buildout]
parts=
#  zope2
  plone
  instance
  roadrunner
develop=
  src/test_package
  src/preloaded_package
  %s/..
eggs =
  elementtree
  test_package
  preloaded_package
  roadrunner
eggs-directory=/Users/jbb/.buildout/eggs
download-directory=/Users/jbb/.buildout/downloads
download-cache=/Users/jbb/.buildout/download-cache

[plone]
recipe = plone.recipe.plone

[zope2]
#recipe = plone.recipe.zope2install
#url = ${plone:zope2-url}
location=/Users/jbb/co/shared_plone3/parts/zope2

[instance]
recipe = plone.recipe.zope2instance
zope2-location = ${zope2:location}
user = admin:admin
http-address = 8080
eggs =
    ${buildout:eggs}
    ${plone:eggs}
products =
#    /Users/jbb/co/shared_plone3/parts/plone
    ${plone:products}

[roadrunner]
recipe = roadrunner:plone
#preload-packages = preloaded_package
package-under-test = test_package
""" % os.path.dirname(__file__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
