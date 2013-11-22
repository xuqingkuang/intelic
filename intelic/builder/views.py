from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import BaseDetailView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from intelic.account.views import LoginRequiredMixin

import models, forms

class TitleMixin(object):
    def set_title(self, title):
        self.title = title

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        if getattr(self, 'title'):
            context['title'] = self.title
        return context

# Create your views here.

class BuildListView(LoginRequiredMixin, TitleMixin, ListView):
    model = models.Build
    title = _('Build list')

class BuildCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = models.Build
    title = _('Build create')
    form_class = forms.BuildCreateModelForm

    def get_form(self, form_class):
        form = super(BuildCreateView, self).get_form(form_class)
        if self.request.method == "POST":
            form.update_by_product(product = self.request.REQUEST['product'])
        return form

    def form_valid(self, form):
        """
        Add the extra component to the build
        """
        self.object = form.save() 
        component_form_class = getattr(forms, self.object.product.form_class.name)
        component_form = component_form_class(
            self.request.POST,
            init_baseline = self.object.baseline,
            init_product = self.object.product,
        )
        if component_form.is_valid():
            component_form.save(build_instance=self.object)
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(component_form)

class BuildDetailView(LoginRequiredMixin, TitleMixin, DetailView):
    model = models.Build
    
    def get_object(self, queryset=None):
        obj = super(BuildDetailView, self).get_object(queryset)
        self.set_title(obj.name)
        return obj

class BuildConfigDownloadView(LoginRequiredMixin, BaseDetailView):
    model = models.Build

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        content = self.object.get_config_file_content()
        response = HttpResponse(content, mimetype='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s.txt' % (
            self.object.slug
        )
        return response