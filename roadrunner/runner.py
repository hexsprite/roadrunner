"""
roadrunner (or rr)

aka. looping testrunner with environment preloading for test-driven development

preloads a standard Zope & Plone test environment compatible with
PloneTestCase.

Tests are then run in a loop.  You are given a shell-like environment with
command history where you can select different tests, etc.

Limitiations
============

Because it preloads the Plone environment you won't be able to see changes
to the Core Plone components.  However, it should see all changes in your
application code which is what you will most likely be changing anyways.
Unless you are a core developer.

Theoretically this should be able to work with any test environment (eg. 
Django, TG, Twisted).

I eventually plan to do this, and would accept any patches in the meantime
if anyone feels so inclined.

Author
======

Jordan Baker <jbb@scryent.com>

TODO
====

- ability to preload any arbitrary layers, plus some presets like --plone or --grok
- hooks for fixture configuration?
- tests... how ironic this code has none, but it started as a proof of concept
"""
from zope.testing import testrunner
import os, sys, time
import shlex

try:
    import readline
    HAVE_READLINE=True
except:
    HAVE_READLINE=False
    
def run_commandloop(args):
    while 1:
        cmdline = raw_input("rr> ").strip()
        if cmdline:
            cmdargs = shlex.split(cmdline)
            if cmdargs[0] in ('quit', 'exit'):
                sys.exit(0)
            if cmdargs[0] in ('help', '?'):
                print HELP_MESSAGE
                continue
            if cmdargs[0] == 'test':
                # ok we have some cmdline arguments
                args = cmdargs[1:]
                break
            else:
                print "Unknown command.  Type 'help' for help."
        else:
            print "rr> test " + shlex_join(args)
            break
    return args
    
def main(zope_conf, args=sys.argv):
    sys.argv = ['fakepath'] # Zope configure whines about argv stuff make it shutup
    bootstrap_zope(zope_conf)
    args = args[2:]
    if HAVE_READLINE:
        readline.add_history('test ' + shlex_join(args))

    ## preload test environment
    t1 = time.time()
    setup_layers = preload_plone()
    t2 = time.time()
    preload_time = t2-t1
    print 'Preloading took: %0.3f seconds.' % (preload_time)

    defaults = testrunner_defaults()
    defaults = setup_paths(defaults)
    
    saved_time = 0
    while 1:
        # Test Loop Start
        pid = os.fork()
        if not pid:
            # Run tests in child process
            t1 = time.time()
            rc = testrunner.run(defaults=defaults, args=args,
                                setup_layers=setup_layers)
            t2 = time.time()
            print 'Testrunner took: %0.3f seconds.  ' % ((t2-t1))
            sys.exit(rc)

        else:
            # In parent process
            try:
                status = os.wait()
                # print "\nchild process returned: ", repr(status)
            except OSError:
                print "\nchild process was interrupted!"
            
            args = run_commandloop(args)
            
        # add to saved_time
        # start the test loop over....

def bootstrap_zope(config_file):
    config_file = os.path.abspath(config_file)
    print "Parsing %s" % config_file
    import Zope2
    Zope2.configure(config_file)

def filter_warnings():
    import warnings
    warnings.simplefilter('ignore', Warning, append=True)
filter_warnings()
        
def maybe_quote_args(arg):
    if ' ' in arg:
        return '"' + arg + '"'
    else:
        return arg
    
def shlex_join(args, char=' '):
    l = map(maybe_quote_args, args)    
    return char.join(args)

HELP_MESSAGE = \
"""\
roadrunner help
--------------

exit
    to quit

test <testrunner arguments>
    run the testrunner

help
    this message
    
Press the <return> key to run the test again with the same arguments.

If you have readline you can use that to search your history.
"""

def setup_paths(defaults):
    """
    this code is from Zope's test.py
    """
    # Put all packages found in products directories on the test-path.
    import Products
    products = []
    softwarehome = '/Users/jbb/co/shared_plone3/parts/zope2/lib/python'
    
    for path in Products.__path__:
        # ignore software home, as it already works
        if not path.startswith(softwarehome):
            # get all folders in the current products folder and filter
            # out everything that is not a directory or a VCS internal one.
            folders = [f for f in os.listdir(path) if
                         os.path.isdir(os.path.join(path, f)) and
                         not f.startswith('.') and not f == 'CVS']
            if folders:
                for folder in folders:
                    # look into all folders and see if they have an
                    # __init__.py in them. This filters out non-packages
                    # like for example documenation folders
                    package = os.path.join(path, folder)
                    if os.path.exists(os.path.join(package, '__init__.py')):
                        products.append(package)

    # Put all packages onto the search path as a package. As we only deal
    # with products, the package name is always prepended by 'Products.'
    for product in products:
        defaults += ['--package-path', product, 'Products.%s' % os.path.split(product)[-1]]

    paths = sys.path
    # progname = self.options.progname
    buildout_root = '/Users/jordan/co/myplatform_buildout/trunk' #os.path.dirname(os.path.dirname(progname))

    for path in paths:
        if path != buildout_root:
            defaults += ['--test-path', path]

    return defaults
    
def preload_plone():
    print "Preloading Plone ..."
    from Products.PloneTestCase.layer import PloneSite
    from Products.PloneTestCase import PloneTestCase as ptc
    ptc.setupPloneSite()
    # pre-setup Plone layer
    from zope.testing.testrunner import setup_layer
    setup_layers={}
    setup_layer(PloneSite, setup_layers)
    # delete the plone layer registration so that the testrunner
    # will re-run Plone layer setUp after deferred setups have
    # been registered by the associated tests.
    del setup_layers[PloneSite] 
    return setup_layers

def testrunner_defaults():
    defaults = '--tests-pattern ^tests$ -v'.split()
                  
    return defaults

def register_signal_handlers(pid):
    # propogate signals to child process
    import signal
    # 
    # def interrupt_handler(signum, frame, pid=pid):
    #     try:
    #         print "received interrupt, killing pid %s" % pid
    #         os.kill(pid, signal.SIGKILL)
    #     except OSError, e:
    #         print e, pid
    #     
    # signal.signal(signal.SIGINT, interrupt_handler)
    # # restore signal handler
    # signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    main()