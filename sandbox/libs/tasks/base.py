import django.template
import utils

class Action(object):

    def __init__(self, id, task, label=None, enabled=True):
        self.id = id
        self.html_id = task.prefixed(str(id))
        self.label = label or id.title()
        self.enabled = enabled


class Task(object):
    """
    Base class for all task objects.

    This class puts up the framework for action handling and rendering. It also
    deals with saving state in the session dictionary (albeit in a very trivial
    manner, since it has empty state).
    """

    class_actions = set()
    initial_state = {}
    template = None

# PUBLIC METHODS

    def __init__(self, prefix = "", state=None, data=None):
        self._prefix = prefix
        self._data = data
        self._state = state

    def __getattr__(self, name):
        if name in self.initial_state:
            # name is part of the state of the task
            if hasattr(self, "get_" + name):
                return getattr(self, "get_" + name)()
            else:
                return self._state.get(self.prefixed(name), self.initial_state[name])
        else:
            raise AttributeError("'" + self.__class__.__name__ + "' has no attribute '" + name + "'")

    def __setattr__(self, name, value):
        if name in self.initial_state:
            # name is part of the state of the task
            if hasattr(self, "set_" + name):
                getattr(self, "set_" + name)(value)
            else:
                self._state[self.prefixed(name)] = value
        else:
            super(Task, self).__setattr__(name, value)

    def post(self, request):
        self.process_action(self.extract_action(request.POST))
        return self._state

    def get(self, request):
        return self.render(request)

# PROTECTED METHODS

    @property
    def actions(self):
        """
        Return dictionary tree whose leaves are actions.
        """
        return dict((action_id, Action(action_id, self)) for action_id in self.class_actions)

    @property
    def tabs(self):
        return []

    def process_action(self, action):
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
        _actions = [action for action in utils.traverse(self.actions) \
                                      if action.html_id in posted]

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
    initial_state = {"current_subtask": 0}

# PUBLIC METHODS

    def __init__(self, prefix="", state=None, data=None):
        self._prefix = prefix
        self._state = state
        self._data = data
        self.init_subtasks()

    def __repr__(self):
        result = "["
        mark = lambda index: "*" if (self._current_subtask == index) else ""
        result += ", ".join(mark(i) + task.__repr__() \
                  for (i, task) in enumerate(self._subtasks))
        result += "]"
        return result

# PRIVATE

    def init_subtasks(self):
        self._subtasks = [cls(self._prefix + str(i) + "_", self._state, self._data) \
                          for (i, cls) in enumerate(self.__class__.subtasks)]

    def set_current_subtask(self, value):
        if 0 <= value and value < len(self._subtasks):
            self._state[self.prefixed("current_subtask")] = unicode(value)
        else:
            raise ValueError("Current subtask specified by an out-of-range index.")

    def get_current_subtask(self):
        return int(self._state.get(self.prefixed("current_subtask"), \
                                   self.initial_state["current_subtask"]))


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
