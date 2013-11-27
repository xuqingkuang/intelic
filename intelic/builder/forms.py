from django import forms
from django.utils.translation import ugettext as _
import models
from pprint import pprint
class BuildCreateModelForm(forms.ModelForm):
    baseline  = forms.ModelChoiceField(queryset = models.Baseline.objects.none())

    class Meta:
        model = models.Build
        fields = ('product', 'baseline')

    def update_by_product(self, product):
        self.fields['baseline'].queryset = models.Baseline.objects.filter(product__pk = product)

class BaseComponentForm(forms.Form):
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        # Stackoverflow: http://stackoverflow.com/questions/1941812/django-error-got-multiple-values-for-keyword-argument
        init_product = kwargs.pop('init_product')
        init_baseline = kwargs.pop('init_baseline')

        super(BaseComponentForm, self).__init__(*args, **kwargs)
        self._set_fields(init_product, init_baseline)

    def _set_fields(self, init_product, init_baseline):
        component_queryset = models.Component.objects.all()
        defualt_component_value_queryset = models.DefaultComponentValue.objects.filter(
            product = init_product
        ).select_related('component_type')
        for field_name in self.fields:
            self.fields[field_name].queryset = models.Component.objects.filter(
                type__slug = field_name,
                product = init_product,
                baseline = init_baseline,
                is_active = True,
            )
            # Hacking the field for replace 'Default' empty label
            for default_component_value in defualt_component_value_queryset:
                if default_component_value.component_type.slug == field_name:
                    self.fields[field_name].empty_label = default_component_value.default_value
                    break
                else:
                    self.fields[field_name].empty_label = _('Default')

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['components'] = []
        for field_name in self.fields:
            if cleaned_data.get(field_name):
                cleaned_data['components'].append(cleaned_data[field_name])
        return cleaned_data

    def save(self, *args, **kwargs):
        build_instance = kwargs.pop('build_instance')
        build_instance.save_components(self.cleaned_data['components'])

class BaseBuildComponentForm(BaseComponentForm):
    touch = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    display = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    audio = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    camera = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    wifi = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    sensor = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
