
from sandbox.libs import tasks

def numbered_task_builder(n):

    class NumberedTask(tasks.AtomicTask):

        number = n

        def __init__(self, prefix="", storage=None):
            super(NumberedTask, self).__init__(prefix, storage)
            self.label = self.__class__.__name__ + "_" + str(self.number)

        def restore_state(self, storage):
            pass

        def save_state(self, storage):
            pass

        def render(self, request):
            return "<b>" + str(self.__class__.number) + "</b>"

    return NumberedTask


class TestTask(tasks.SequentialTask):

    template = 'test_task.html'
    subtasks = [numbered_task_builder(i) for i in range(4)]




