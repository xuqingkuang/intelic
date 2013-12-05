from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import BaseDetailView, DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from intelic.account.views import LoginRequiredMixin

import os.path
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
    context_object_name = 'builds'

class BuildCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = models.Build
    title = _('Build create')
    form_class = forms.BuildCreateModelForm

    def get_form(self, form_class):
        form = super(BuildCreateView, self).get_form(form_class)
        if self.request.method == "POST" and self.request.REQUEST.get('product'):
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

class BuildDetailContentView(LoginRequiredMixin, DetailView):
    model = models.Build
    template_name = 'builder/build_detail_content.html'

    def get_object(self, queryset=None):
        obj = super(BuildDetailContentView, self).get_object(queryset)
        obj.update_process()
        return obj

class BuildConfigDownloadView(LoginRequiredMixin, TemplateView):
    model = models.Build
    template_name = 'builder/components.txt'
    content_type = 'application/octet-stream'

    def get_context_data(self, **kwargs):
        context = super(BuildConfigDownloadView, self).get_context_data(**kwargs)
        context['product'] = models.Product.objects.get(
            pk = self.request.REQUEST.get('product')
        )
        context['baseline'] = models.Baseline.objects.get(
            pk = self.request.REQUEST.get('baseline')
        )
        if self.request.REQUEST.get('pmic'):
            context['pmics'] = models.Baseline.objects.filter(
                pk__in = self.request.REQUEST.getlist('pmic')
            )
        component_form_class = getattr(forms, context['product'].form_class.name)
        component_form = component_form_class(
            self.request.REQUEST,
            init_product = context['product'],
            init_baseline = context['baseline'],
        )
        if component_form.is_valid():
            context['components'] = []
            # FIXME: Hard code find component type here, it's a bug.
            component_types = models.ComponentType.objects.all()
            for component_type in component_types:
                for component in component_form.cleaned_data['components']:
                    if component.type == component_type:
                        context['components'].append(component)
                        break;
                else:
                    context['components'].append({
                        'type': component_type,
                        'name': None
                    })
        return context
