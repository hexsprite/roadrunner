from setuptools import setup, find_packages
import sys, os

version = '0.2.3'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n'
        # 'Download\n'
        # '**********************\n'
        )

file('doc.txt', 'w').write(long_description)

setup(name='roadrunner',
      version=version,
      description="testrunner for test-driven development",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='zope buildout TDD testing',
      author='Jordan Baker',
      author_email='jbb@scryent.com',
      url='',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'zc.recipe.egg',
          'zc.buildout',
      ],
      entry_points = """
        [console_scripts]
        rrplone = roadrunner.runner:plone
        [zc.buildout]
        plone = roadrunner:Plone
      """
      )
