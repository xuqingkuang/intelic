from django import forms
import models

class JobCreateModelForm(forms.ModelForm):
    product  = forms.ChoiceField()

    class Meta:
        model = models.Job
        fields = ('baseline', 'product')

    def __init__(self, *args, **kwargs):
        super(JobCreateModelForm, self).__init__(*args, **kwargs)
        self.component_fields = ('touch', 'display', 'audio', 'camera', 'wifi', 'sensor')

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        pass

class BaseComponentForm(forms.Form):
    class Meta:
        abstract = True
    
    def __init__(self, init_baseline, init_product, *args, **kwargs):
        super(BaseComponentForm, self).__init__(*args, **kwargs)
        component_queryset = models.Component.objects.all()
        for field_name in self.fields:
            self.fields[field_name].queryset = models.Component.objects.filter(
                type__slug = field_name,
                baseline = init_baseline,
                product = init_product,
                is_active = True,
            )

class BaseJobComponentForm(BaseComponentForm):
    touch = forms.ModelChoiceField(queryset = models.Component.objects.all())
    display = forms.ModelChoiceField(queryset = models.Component.objects.all())
    audio = forms.ModelChoiceField(queryset = models.Component.objects.all())
    camera = forms.ModelChoiceField(queryset = models.Component.objects.all())
    wifi = forms.ModelChoiceField(queryset = models.Component.objects.all())
    sensor = forms.ModelChoiceField(queryset = models.Component.objects.all())
