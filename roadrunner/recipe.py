import os, fnmatch, shutil
from zc.recipe.egg.egg import Scripts

class RoadrunnerRecipe(Scripts):
    """
    generic options:
    packages_under_test = list of regex packages
    preload_packages = list of packages
    """
   
    def __init__(self, buildout, name, options):
        super(RoadrunnerRecipe, self).__init__(buildout, name, options)
        self.instance_part = buildout[options.get('zope2-instance', 'instance')]
        self.part_dir = self.buildout['buildout']['directory'] + "/parts/" + self.name
        self.packages_under_test = options.get('packages-under-test', '').split()

    def install(self):
        """
        emulate this sort of thing:
        [roadrunner]
        recipe = zc.recipe.egg
        eggs =
            ${instance:eggs}
            roadrunner
        extra-paths = 
        initialization =
            conf_file = "${instance:location}/etc/zope-roadrunner.conf"
        arguments = conf_file, "${instance:zope2-location}", "${buildout:directory}"
        """
        options = self.options
        vars = dict(
            instance_location = self.instance_part['location'],
            zope2_location = self.instance_part['zope2-location'],
            preload_modules = options.get('preload-modules', ''),
            packages_under_test = self.packages_under_test,
            buildout_home = self.buildout['buildout']['directory'],
            part_dir = self.part_dir
        )

        options['eggs'] = ( '\n'.join(options.get('eggs', '').split() + 
            self.instance_part['eggs'].split() + ['roadrunner']) )
        options['initialization'] = """\
zope_conf = '%(part_dir)s/etc/zope.conf'
preload_modules = '%(preload_modules)s'
packages_under_test = %(packages_under_test)s
zope2_location = '%(zope2_location)s'
buildout_home = '%(buildout_home)s'
part_dir = '%(part_dir)s'
sys.path.append(zope2_location + "/lib/python")
""" % vars
        options['arguments'] = 'zope_conf, preload_modules, packages_under_test, zope2_location, buildout_home, part_dir'
        # TODO: extra_paths doesn't seem to work...?
        options['extra_paths']= "%(zope2_location)s/lib/python" % vars
        options['scripts'] = 'rrplone=' + self.name 
        
        return super(RoadrunnerRecipe, self).install()
        
    def update(self):
        return self.install()
        
class RoadrunnerPloneRecipe(RoadrunnerRecipe):
    """
    zope recipe options:
    
    zope_instance
    """
    
    # def __init__(self, buildout, name, options):
    #     super(RoadrunnerPloneRecipe, self).__init__(buildout, name, options)

    def is_package_under_test(self, filepath):
        for pattern in self.packages_under_test:
            if fnmatch.fnmatch(filepath, '*' + pattern + '*'):
                return True
        return False
        
    def configure_roadrunner_instance(self):
        """
        copy a zope instance to work with roadrunner packages under test
        """
        if os.path.exists(self.part_dir):
            shutil.rmtree(self.part_dir)

        instance = self.instance_part['location']
        shutil.copytree(instance, self.part_dir)
        
        # filter out packages under test to load from site.zcml
        zcml_dest = self.part_dir + "/etc/package-includes"
        for dirpath, dirnames, filenames in os.walk(zcml_dest):
            for filename in filenames:
                if self.is_package_under_test(filename):
                    path = dirpath + "/" + filename
                    os.remove(path)
        
        # rewrite the old paths => new in zope.conf
        zopeconf_dest =  "%s/etc/zope.conf" % self.part_dir
        zopeconf = file(zopeconf_dest).read()
        zopeconf = zopeconf.replace(instance, self.part_dir)
        file(zopeconf_dest, "w").write(zopeconf)
    
    def install(self):
        self.configure_roadrunner_instance()
        
        return super(RoadrunnerPloneRecipe, self).install() + [self.part_dir]
