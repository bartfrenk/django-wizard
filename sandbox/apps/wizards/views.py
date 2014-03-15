from django.views.generic import View
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render
from sandbox.apps.wizards import definitions
from urllib import urlencode

class TaskView(View):
    template_name = 'task_wrapper.html'

    def get(self, request, *args, **kwargs):
        # initialize task session storage
        request.session['data'] = {}
        state = request.GET.dict()
        task = definitions.TestTask(state=state, data=request.session['data'])
        return render(request, self.template_name, {'task_html': task.get(request)})

    def post(self, request, *args, **kwargs):
        [url, qs] = request.META["HTTP_REFERER"].split("?")
        state = QueryDict(qs).dict()
        task = definitions.TestTask(state=state, data=request.session['data'])
        # session is not considered to be modified when no dictionary keys
        # have been assigned or deleted, and thus not saved, unless forced
        state = task.post(request)
        request.session.modified = True
        return HttpResponseRedirect(url + "?" + urlencode(state))

