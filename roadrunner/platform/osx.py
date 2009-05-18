import sys

def avoid_core_functions():
    """
    http://hexsprite.lighthouseapp.com/projects/21973-roadrunner/tickets/4

    Using urllib under OSX triggers this error.

    This patch causes Python to skip using the ic module under OSX to avoid
    triggering this error.

     __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__()
    is the worst error name ever

    Who knows, maybe there's a better way to solve this?
    """
    import sys
    # just importing the ic module causes the error
    sys.modules['ic'] = None

def patch_osx():
    avoid_core_functions()

if sys.platform == 'darwin':
    patch_osx()

