from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext as _
from intelic.account.views import LoginRequiredMixin

import models, forms

# Create your views here.

class JobListView(LoginRequiredMixin, ListView):
    model = models.Job
    template_name = 'builder/job_list.html'
    title = _('Job list')

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['title'] = _('Job list')
        # TODO: Completed related items field
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = models.Job
    title = _('Job create')
    form_class = forms.JobCreateModelForm
