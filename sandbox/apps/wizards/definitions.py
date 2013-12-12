
from sandbox.libs import tasks


class TestTask(tasks.SequentialTask):

    template = 'test_task.html'

    def __init__(self, length, prefix="", state=None, data=None, posted=None):
        self.length = length
        super(TestTask, self).__init__(prefix, state, data, posted)

    def set_subtasks(self, prefix, *args, **kwargs):
        self._subtasks = [NumberedTask(i, prefix) for i in range(self.length)]


class NumberedTask(tasks.AtomicTask):

    def __init__(self, number, prefix="", state=None, data=None, posted=None):
        super(NumberedTask, self).__init__(prefix, state, data, posted)
        self.number = number

    def restore_state(self, storage):
        pass

    def save_state(self, storage):
        pass

    def render(self):
        return "<b>" + str(self.number) + "</b>"
