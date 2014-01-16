from collections import OrderedDict
import base


class SequentialTask(base.CompositeTask):

    class_actions = {'previous', 'next'}
    template = "sequential_task.html"

# PROTECTED

    @property
    def actions(self):
        actions = super(SequentialTask, self).actions
        actions['tabs'] = OrderedDict((tab, self.prefixed(tab))
                                      for (index, tab) in enumerate(self.tabs))
        return actions

    @property
    def tabs(self):
        tab_list = []
        for subtask in self._subtasks:
            tab_list += subtask.tabs
        return tab_list

    def process_action(self, action):
        if action == 'previous':
            self.set_current_subtask(max(0, self._current_subtask - 1))
        elif action == 'next':
            self.set_current_subtask(min(len(self._subtasks) - 1, self._current_subtask + 1))
        elif action is None:
            pass
        else:
            raise ValueError("Cannot handle action " + str(action) + ".")

    def is_complete(self):
        return all(subtask.is_complete() for subtask in self._subtasks)

    def get_context(self, request):
        context = super(SequentialTask, self).get_context()
        context.update({'subtask_html':
                        self._subtasks[self._current_subtask].render(request)})
        return context



class DisjunctiveTask(base.CompositeTask):

    def is_complete(self):
        # task is complete if at least one of the subtasks is complete
        return any(subtask.is_complete() for subtask in self._subtasks)


class SimultaneousTask(base.CompositeTask):
    pass


if __name__ == "__main__":
    class SubTask(SequentialTask):
        subtasks = [base.AtomicTask for _ in range(4)]
    class TestTask(SequentialTask):
        subtasks = [SubTask for _ in range(2)]
    task = TestTask()
    print(task)
    task.process_action("next")
    print(task)
    print(task.is_complete())
    print(task.actions)
    print(task.tabs)
