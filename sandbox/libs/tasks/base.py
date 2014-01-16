import django.template
import utils


class Task(object):
    """
    Base class for all task objects.

    This class puts up the framework for action handling and rendering. It also
    deals with saving state in the session dictionary (albeit in a very trivial
    manner, since it has empty state).
    """

    class_actions = set()
    template = None

# PUBLIC METHODS

    def __init__(self, prefix = "", storage=None):
        self._prefix = prefix
        self._storage = storage
        self.restore()

    def post(self, request):
        self.process_action(self.extract_action(request.POST))
        self.save()
        return self.render(request)

    def get(self, request):
        self.save()
        return self.render(request)

# PROTECTED METHODS

    @property
    def actions(self):
        """
        Return dictionary tree whose leaves map action names to action identifiers.
        """
        return dict((action, self.prefixed(action)) for action in self.class_actions)

    @property
    def tabs(self):
        return []

    def process_action(self, action):
        pass

    def restore(self):
        pass

    def save(self):
        pass

    def get_context(self):
        return {'actions': self.actions}

    def is_complete(self):
        return True

# PRIVATE METHODS

    def extract_action(self, posted):
        """
        Retrieve the action name for the actions taken by the user (i.e. submitted
        through an http post request).
        """
        _actions = [action for (action, html_id) in utils.flatten(self.actions).items() \
                                                 if html_id in posted]

        if len(_actions) > 1:
            raise ValueError('Cannot process more than one action.')
        elif len(_actions) == 0:
            return None
        else:
            return _actions[0]

    def prefixed(self, string):
        return self._prefix + string

    def render(self, request):
        template = django.template.loader.get_template(self.template)
        return template.render(django.template.Context(self.get_context(request)))


class CompositeTask(Task):
    """
    Base class for tasks consisting of multiple subtasks.
    """
    subtasks = []
    initial_subtask = 0

# PUBLIC METHODS

    def __init__(self, prefix="", storage=None):
        self._prefix = prefix
        self._storage = storage
        self.init_subtasks()
        self.restore()

    def __repr__(self):
        result = "["
        mark = lambda index: "*" if (self._current_subtask == index) else ""
        result += ", ".join(mark(i) + task.__repr__() \
                  for (i, task) in enumerate(self._subtasks))
        result += "]"
        return result

# PROTECTED METHODS

    def save(self):
        self._storage['state'][self.prefixed('current_subtask')] = self._current_subtask

    def restore(self):
        state = self._storage.get('state') if self._storage else None
        if state is None:
            self._current_subtask = 0
        else:
            self.set_current_subtask(state.get(self.prefixed('current_subtask'), 0))

# PRIVATE

    def init_subtasks(self):
        self._subtasks = [cls(self._prefix + str(i) + "_", self._storage) \
                          for (i, cls) in enumerate(self.__class__.subtasks)]

    def set_current_subtask(self, index):
        if 0 <= index and index < len(self._subtasks):
            self._current_subtask = index
        else:
            raise ValueError("Current subtask specified by an out-of-range index.")


class AtomicTask(Task):
    """
    Base class for atomic tasks.
    """
    @property
    def tabs(self):
        return [getattr(self, 'label', self.__class__.__name__)]


if __name__ == "__main__":
    class TestTask(CompositeTask):
        subtasks = [AtomicTask, AtomicTask]
    task = TestTask()
    print(task)
