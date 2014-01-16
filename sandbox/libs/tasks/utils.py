
class SuppressErrors(object):

    def __init__(self, *exceptions):
        if not exceptions:
            exceptions = (Exception,)
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_class, exc_instance, traceback):
        if isinstance(exc_instance, self.exceptions):
            return True
        return False

def flatten(tree):
    """
    Return the leaves of the action tree.
    """
    # TODO: make this generic by flattening the action tree
    leaves = {}

    def _flatten(node):
        for (key, value) in node.items():
            if isinstance(value, dict):
                _flatten(value)
            else:
                leaves[key] = value

    _flatten(tree)
    return leaves
