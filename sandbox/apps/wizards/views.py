from django.views.generic import View
from django.shortcuts import render
from sandbox.apps.wizards import definitions


class TaskView(View):
    template_name = 'task_wrapper.html'

    def get(self, request, *args, **kwargs):
        task = definitions.TestTask(length=5)
        request.session['state'] = {}
        task.save_state(request.session['state'])
        return render(request, self.template_name, {'task_html': task.render()})

    def post(self, request, *args, **kwargs):
        task = definitions.TestTask(length=5, state=request.session.get('state'),
                                    posted=request.POST)
        request.session['state'] = {}
        task.save_state(request.session['state'])
        return render(request, self.template_name, {'task_html': task.render()})
