import django.template


class Task(object):
    """
    Base class for all task objects.

    This class puts up the framework for action handling and rendering. It also
    deals with saving state in the session dictionary (albeit in a very trivial
    manner, since it has no state).
    """

    actions = set()

    def __init__(self, prefix = "", state = None, data = None, posted = None):
        self._prefix = prefix
        self.restore_state(state)
        self.process_action(self.extract_action(posted or {}))

    def render(self):
        # TODO: This method should probably be passed the request object.
        # This avoids having to initialize to much afterwards.
        _template = django.template.loader.get_template(self.template)
        return _template.render(django.template.Context(self.get_context()))

    def extract_action(self, posted):
        """
        Retrieve the action name for the actions taken by the user (i.e. submitted
        through an http post request).
        """
        _actions = [name for (name, id) in self.get_flat_actions().items() if id in posted]
        if len(_actions) > 1:
            raise ValueError('Cannot process more than one action.')
        elif len(_actions) == 0:
            return None
        else:
            return _actions[0]

    def process_action(self, action):
        pass

    def get_flat_actions(self):
        """
        Return the leaves of the action tree.
        """
        # TODO: make this generic by flattening the action tree
        return self.get_struct_actions()

    def get_struct_actions(self):
        """
        Return dictionary tree whose leaves map action names to action identifiers.
        """
        return dict((action, self.prefixed(action)) for action in self.actions)

    def get_context(self):
        return {'actions': self.get_struct_actions()}

    def prefixed(self, string):
        return self._prefix + string

    def save_state(self, storage):
        pass

    def restore_state(self, storage):
        pass

    def get_tab_list(self):
        return [getattr(self, 'label', self.__class__.__name__)]

    def is_complete(self):
        return True


class CompositeTask(Task):
    """
    Base class for tasks consisting of multiple subtasks.
    """

    def __init__(self, prefix = "", state = None, data = None, posted = None):
        self.set_subtasks(prefix)
        super(CompositeTask, self).__init__(prefix, state, data, posted)

    def save_state(self, storage):
        storage[self.prefixed('current_subtask')] = self._current_subtask

    def restore_state(self, state):
        if state is None:
            self._current_subtask = 0
        else:
            self.set_current_subtask(state.get(self.prefixed('current_subtask'), 0))

    def set_current_subtask(self, index):
        if 0 <= index and index < len(self._subtasks):
            self._current_subtask = index
        else:
            raise ValueError("Current subtask specified by an out-of-range index.")

    def get_current_subtask(self):
        return self._subtasks[self._current_subtask]

    def set_subtasks(self, *args, **kwargs):
        raise NotImplementedError


class AtomicTask(Task):
    """
    Base class for atomic tasks.
    """
    pass
