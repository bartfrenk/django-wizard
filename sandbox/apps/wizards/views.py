from django.views.generic import View
from django.shortcuts import render
from sandbox.apps.wizards import definitions


class TaskView(View):
    template_name = 'task_wrapper.html'

    def get(self, request, *args, **kwargs):
        # initialize task session storage
        request.session['state'] = {}
        request.session['data'] = {}
        task = definitions.TestTask(prefix='tsk_', storage=request.session)
        return render(request, self.template_name, {'task_html': task.get(request)})

    def post(self, request, *args, **kwargs):
        task = definitions.TestTask(prefix="tsk_", storage=request.session)
        # session is not considered to be modified when no dictionary keys
        # have been assigned or deleted, and thus not saved, unless forced
        request.session.modified = True
        return render(request, self.template_name, {'task_html': task.post(request)})
