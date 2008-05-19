Testing roadrunner
------------------

First off let's create a sample test for roadrunner to run

write('buildout.cfg', """\
[buildout]
parts=roadrunner
develop=.

[roadrunner]
recipe=zc.recipe.egg
""")


TODO
====

- ability to preload any arbitrary layers, plus some presets like --plone or --grok
- hooks for fixture configuration?
- tests... how ironic this code has none, but it started as a proof of concept
- prevent layer destruction for an added half second

