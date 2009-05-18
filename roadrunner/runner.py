"""
roadrunner
"""
from roadrunner import testrunner
import os, sys, time, signal, shlex

# apply platform specific patches
import roadrunner.platform; roadrunner

try:
    import readline
    HAVE_READLINE=True
except:
    HAVE_READLINE=False

def run_commandloop(args):
    while 1:
        cmdline = raw_input("rr> ").strip()

        if cmdline:
            try:
                cmdargs = shlex.split(cmdline)
            except ValueError: # problem parsing line
                print "Cmdline syntax error"
                continue
                
            if cmdargs[0] in ('quit', 'exit'):
                sys.exit(0)

            if cmdargs[0] in ('help', '?'):
                print HELP_MESSAGE
                continue

            if cmdargs[0] == 'debug':
                import pdb
                pdb.set_trace()
                continue

            if cmdargs[0] == 'python':
                from code import InteractiveConsole
                ic = InteractiveConsole(locals=locals())
                ic.interact("Python Debug shell")
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

# 
def plone(zope_conf, preload_modules, packages_under_test, zope2_location, buildout_home, part_dir, args=sys.argv):
    software_home = zope2_location + "/lib/python"
    sys.argv = sys.argv[0:1] # Zope configure whines about argv stuff make it shutup
    bootstrap_zope(zope_conf)
    args = args[1:]
    if HAVE_READLINE:
        readline.add_history('test ' + shlex_join(args))

    ## preload test environment
    t1 = time.time()
    setup_layers = preload_plone(part_dir)
    t2 = time.time()
    preload_time = t2-t1
    print 'Preloading took: %0.3f seconds.' % (preload_time)

    defaults = testrunner_defaults()
    defaults = setup_paths(defaults, software_home, buildout_home)
    
    # start out negative because the first run through we don't actually save time
    # since we would have had to load it anyways
    saved_time = -preload_time
    
    ignore_signal_handlers()
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while 1:
        # Test Loop Start
        pid = os.fork()
        if not pid:
            # Run tests in child process
            t1 = time.time()
            rc = testrunner.run(defaults=defaults, args=[sys.argv[0]] + args,
                                setup_layers=setup_layers)
            t2 = time.time()
            print 'Testrunner took: %0.3f seconds.  ' % ((t2-t1))
            sys.exit(rc)

        else:
            # In parent process
            try:
                register_signal_handlers(pid)
                try:
                    # os.wait() can throw OSError
                    status = os.wait()
                    saved_time += preload_time
                    if saved_time:
                        print "Saved time so far: %0.3f seconds." % saved_time
                except OSError:
                    # TODO: maybe need something smarter here, maybe not?
                    pass
            finally:
                ignore_signal_handlers()
                # TODO: deal with windows
                os.system("stty echo") # HACK
                
            args = run_commandloop(args)

        # start the test loop over....

def bootstrap_zope(config_file):
    config_file = os.path.abspath(config_file)
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

def setup_paths(defaults, software_home, buildout_home):
    """
    this code is from Zope's test.py
    """
    # Put all packages found in products directories on the test-path.
    import Products
    products = []
    
    for path in Products.__path__:
        # ignore software home, as it already works
        if not path.startswith(software_home):
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
    for path in paths:
        if path != buildout_home:
            defaults += ['--test-path', path]

    return defaults

def preload_plone(conf):
    print "Preloading Plone ..."
    from Products.PloneTestCase.layer import PloneSite
    from Products.PloneTestCase import PloneTestCase as ptc
    ptc.setupPloneSite()
    # pre-setup Plone layer
    setup_layers={}
    testrunner.setup_layer(PloneSite, setup_layers)
    # delete the plone layer registration so that the testrunner
    # will re-run Plone layer setUp after deferred setups have
    # been registered by the associated tests.
    del setup_layers[PloneSite] 
    return setup_layers

def testrunner_defaults():
    defaults = '--tests-pattern ^tests$ -v'.split()
    defaults += ['-k']
    
    return defaults

original_signal_handler = None
def register_signal_handlers(pid):
    "propogate signals to child process"
    def interrupt_handler(signum, frame, pid=pid):
        try:
            os.kill(pid, signal.SIGKILL)
            print # clear the line
        except OSError, e:
            print str(e), pid

    signal.signal(signal.SIGINT, interrupt_handler)

def default_int_handler(signum, frame):
    print "\nInterrupt received. Type 'exit' to quit."
    
def ignore_signal_handlers():
    "restore signal handler"
    signal.signal(signal.SIGINT, default_int_handler)

