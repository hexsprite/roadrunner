from zope.testing.testrunner.runner import Runner, CanNotTearDown, run_layer, tear_down_unneeded
import zope.testing.testrunner.interfaces

class Roadrunner(Runner):
    def __init__(self, defaults=None, args=None, found_suites=None,
                 options=None, script_parts=None, setup_layers=None):
        self.defaults = defaults
        self.args = args
        self.found_suites = found_suites
        self.options = options
        self.script_parts = script_parts
        self.failed = True

        self.ran = 0
        self.failures = []
        self.errors = []

        self.show_report = True
        self.do_run_tests = True

        self.features = []

        self.tests_by_layer_name = {}
        
        # ADDED: allow Roadrunner pass in layers that were setup previously
        if setup_layers:
            self.setup_layers = setup_layers
        else:
            self.setup_layers = {}
    
    def run_tests(self):
        """Run all tests that were registered.

        Returns True if there where failures or False if all tests passed.

        """
        # CHANGED: get setup layers from attribute
        setup_layers = self.setup_layers
        layers_to_run = list(self.ordered_layers())
        should_resume = False

        while layers_to_run:
            layer_name, layer, tests = layers_to_run[0]
            for feature in self.features:
                feature.layer_setup(layer)
            try:
                self.ran += run_layer(self.options, layer_name, layer, tests,
                                      setup_layers, self.failures, self.errors)
            except zope.testing.testrunner.interfaces.EndRun:
                self.failed = True
                return
            except CanNotTearDown:
                if not self.options.resume_layer:
                    should_resume = True
                    break

            layers_to_run.pop(0)
            if self.options.processes > 1:
                should_resume = True
                break

        if should_resume:
            setup_layers = None
            if layers_to_run:
                self.ran += resume_tests(
                    self.script_parts, self.options, self.features,
                    layers_to_run, self.failures, self.errors)

        if setup_layers:
            if self.options.resume_layer is None:
                self.options.output.info("Tearing down left over layers:")
            tear_down_unneeded(self.options, (), setup_layers, True)

        self.failed = bool(self.import_errors or self.failures or self.errors)
