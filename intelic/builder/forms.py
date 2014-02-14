from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import models
from pprint import pprint

class BuildCreateModelForm(forms.ModelForm):
    author    = forms.ModelChoiceField(
        queryset = User.objects.all(),
        widget = forms.HiddenInput()
    )
    baseline  = forms.ModelChoiceField(queryset = models.Baseline.objects.none())

    class Meta:
        model = models.Build
        fields = ('author', 'product', 'pmic', 'baseline')

    def __init__(self, *args, **kwargs):
        super(BuildCreateModelForm, self).__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].empty_label = _('NULL')
            
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
            self.fields[field_name].empty_label = _('NULL')
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
    memory = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    emmc = forms.ModelChoiceField(
        label = 'EMMC',
        queryset = models.Component.objects.all(), required = False
    )
    touch = forms.ModelChoiceField(
        label = 'Touch controller',
        queryset = models.Component.objects.all(), required = False
    )
    panel = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    codec = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    camera1 = forms.ModelChoiceField(
        label = 'Camera module 1',
        queryset = models.Component.objects.all(), required = False
    )
    camera2 = forms.ModelChoiceField(
        label = 'Camera module 2',
        queryset = models.Component.objects.all(), required = False
    )
    wifi_bluetooth = forms.ModelChoiceField(
        label = 'WIFI/Bluetooth',
        queryset = models.Component.objects.all(), required = False
    )
    gps = forms.ModelChoiceField(
        label = 'GPS',
        queryset = models.Component.objects.all(), required = False
    )
    nfc = forms.ModelChoiceField(
        label = 'NFC',
        queryset = models.Component.objects.all(), required = False
    )
    wwan = forms.ModelChoiceField(
        label = 'WWAN',
        queryset = models.Component.objects.all(), required = False
    )
    sensor_hub = forms.ModelChoiceField(
        label = 'Sensor HUB',
        queryset = models.Component.objects.all(), required = False
    )
    als_sensor = forms.ModelChoiceField(
        label = 'ALS Sensor',
        queryset = models.Component.objects.all(), required = False
    )
    gyro_sensor = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    accelerator_sensor = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    magnetic_sensor = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    sar_sensor = forms.ModelChoiceField(
        label = 'Sar sensor',
        queryset = models.Component.objects.all(), required = False
    )
    pressure_sensor = forms.ModelChoiceField(
        queryset = models.Component.objects.all(), required = False
    )
    uv_sensor = forms.ModelChoiceField(
        label = 'UV Sensor',
        queryset = models.Component.objects.all(), required = False
    )
