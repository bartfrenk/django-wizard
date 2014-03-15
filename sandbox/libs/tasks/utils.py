
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
    leaves = {}

    def _flatten(node):
        for (key, value) in node.items():
            if isinstance(value, dict):
                _flatten(value)
            else:
                leaves[key] = value

    _flatten(tree)
    return leaves


def traverse(tree):

    if isinstance(tree, list):
        for item in tree:
            yield item
    elif isinstance(tree, dict):
        for branch in tree.values():
            for item in traverse(branch):
                yield item
    else:
        yield tree


if __name__ == "__main__":
    tree = {'a': [1,2,3], 'b':[4,5,6], 'c': {'d': [7,8], 'e': 9}}
    print(list(traverse(tree)))

