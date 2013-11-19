from django.views.generic.detail import DetailView
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

# Create your views here.

class UserDashboardView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'auth/user_dashboard.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        context['title'] = _('Dashboard')
        # TODO: Completed related items field
        return context
