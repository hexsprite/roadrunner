
class RoadrunnerRecipe(object):
    """
    [roadrunner]
    recipe = zc.recipe.egg
    eggs =
        ${instance:eggs}
        roadrunner
    extra-paths = ${instance:zope2-location}/lib/python
    initialization =
        conf_file = "${instance:location}/etc/zope-roadrunner.conf"
    arguments = conf_file, "${instance:zope2-location}", "${buildout:directory}"
    """
   
    def __init__(self, buildout, name, options):
        self.name, self.options = name, options
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              options['path'],
                              )
        if not os.path.isdir(os.path.dirname(options['path'])):
            logging.getLogger(self.name).error(
                'Cannot create %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        logging.getLogger(self.name).info(
            'Creating directory %s', os.path.basename(path))
        os.mkdir(path)
        return path

    def update(self):
        pass