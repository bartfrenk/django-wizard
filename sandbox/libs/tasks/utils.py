
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
