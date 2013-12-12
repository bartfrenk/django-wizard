
import base


class SequentialTask(base.CompositeTask):

    template = "sequential_task.html"
    actions = {'previous', 'next'}

    def process_action(self, action):
        if action == 'previous':
            self._current_subtask = max(0, self._current_subtask - 1)
        elif action == 'next':
            self._current_subtask = min(len(self._subtasks) - 1, self._current_subtask + 1)
        elif action is None:
            pass
        else:
            raise ValueError("'Cannot handle action " + str(action) + ".")

    def get_flat_actions(self):
        # TODO: this function should output the flattening of get_actions_for_template
        # TODO: hacked to make it work: add tab actions to the dictionary.
        _actions = super(SequentialTask, self).get_flat_actions()
        return _actions

    def get_struct_actions(self):
        # TODO: make dictionary under tabs ordered of the form (label -> action_id)
        _actions = super(SequentialTask, self).get_struct_actions()
        _actions['tabs'] = [tab for tab in enumerate(self.get_tab_list())]
        return _actions

    def get_tab_list(self):
        tab_list = []
        for subtask in self._subtasks:
            tab_list += subtask.get_tab_list()
        return tab_list

    def set_subtasks(self, *args, **kwargs):
        self._subtasks = args

    def get_context(self):
        context = super(SequentialTask, self).get_context()
        context.update({'subtask': self.get_current_subtask()})
        return context

    def is_complete(self):
        return all(subtask.is_complete() for subtask in self._subtasks)


class DisjunctiveTask(base.CompositeTask):

    def is_complete(self):
        # task is complete if at least one of the subtasks is complete
        return any(subtask.is_complete() for subtask in self._subtasks)


class SimultaneousTask(base.CompositeTask):
    pass
