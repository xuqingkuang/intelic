from django import forms
from django.utils.translation import ugettext as _
import models

class BuildCreateModelForm(forms.ModelForm):
    product  = forms.ModelChoiceField(queryset = models.Product.objects.none())

    class Meta:
        model = models.Build
        fields = ('baseline', 'product')
    
    def update_by_baseline(self, baseline):
        self.fields['product'].queryset = models.Product.objects.filter(baseline__pk = baseline)

class BaseComponentForm(forms.Form):
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        # Stackoverflow: http://stackoverflow.com/questions/1941812/django-error-got-multiple-values-for-keyword-argument
        init_baseline = kwargs.pop('init_baseline')
        init_product = kwargs.pop('init_product')
        
        super(BaseComponentForm, self).__init__(*args, **kwargs)
        component_queryset = models.Component.objects.all()
        for field_name in self.fields:
            self.fields[field_name].queryset = models.Component.objects.filter(
                type__slug = field_name,
                baseline = init_baseline,
                product = init_product,
                is_active = True,
            )

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['components'] = []
        for field_name in self.fields:
            if cleaned_data.get(field_name):
                cleaned_data['components'].append(cleaned_data[field_name])
        return cleaned_data

    def save(self, *args, **kwargs):
        build_instance = kwargs.pop('build_instance')
        for component in self.cleaned_data['components']:
            build_instance.component.add(component)

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
    power = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    i2c = forms.ModelChoiceField(
        label="I2C", queryset = models.Component.objects.all(), required = False
    )
