from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from datetime import datetime

from intelic.jenkins_handler import icjenkinsjob

# Create your models here.

# ##################################################
# Abstract models
# ##################################################

class BaseModel(models.Model):
    name            = models.CharField(verbose_name=_('Name'), max_length=128)
    slug            = models.SlugField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save to make slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        return super(BaseModel, self).save(*args, **kwargs)

# ##################################################
# Product models
# ##################################################

class FormClass(BaseModel):
    pass

class Baseline(BaseModel):
    desc            = models.CharField(
        verbose_name=_('Description'), max_length=255, blank=True, null=True
    )
    is_active       = models.BooleanField(
        verbose_name=_('Is active'), default=True
    )

class Product(BaseModel):
    desc            = models.CharField(
        verbose_name=_('Description'), max_length=255, blank=True, null=True
    )
    form_class      = models.ForeignKey(FormClass, verbose_name=_('Form class'))
    baseline        = models.ManyToManyField(Baseline)
    is_active       = models.BooleanField(
        verbose_name=_('Is active'), default=True
    )

# ##################################################
# Component models
# ##################################################

class ComponentType(BaseModel):
    pass

class Component(BaseModel):
    desc            = models.CharField(
        verbose_name=_('Description'), max_length=255, blank=True, null=True
    )
    type            = models.ForeignKey(ComponentType)
    source          = models.FileField(
        verbose_name=_('Source'), upload_to='uploads/source/', blank=True,
        null=True
    )
    gerrit_url      = models.URLField(
        verbose_name=_('Gerrit URL'), max_length=8192, blank=True, null=True
    )
    baseline        = models.ManyToManyField(
        Baseline, verbose_name=_('Baseline')
    )
    product         = models.ManyToManyField(
        Product, verbose_name=_('Product')
    )
    is_active       = models.BooleanField(
        verbose_name=_('Is active'), default=True
    )

    def upload_source_to_git_repo(self):
        # TODO: Complete the function.
        pass

    def get_gerrit_change_number(self):
        if not self.gerrit_url:
            return None
        return self.gerrit_url.split('/')[-2]

    def save(self, *args, **kwargs):
        """Override save to make slug"""
        if not self.slug:
            self.slug = slugify('%s-%s' % (self.type, self.name))
        return super(Component, self).save(*args, **kwargs)

# ##################################################
# Job models
# ##################################################

class Build(BaseModel):
    created_at      = models.DateTimeField(
        verbose_name=_('Create at'), auto_now_add=True
    )
    baseline        = models.ForeignKey(Baseline, verbose_name=_('Baseline'))
    product         = models.ForeignKey(Product, verbose_name=_('Product'))
    status          = models.CharField(max_length=11, blank=True, null=True)
    message         = models.CharField(max_length=8192, blank=True, null=True)
    progress        = models.IntegerField(default=0)
    component       = models.ManyToManyField(Component)

    def get_absolute_url(self):
        return reverse('build_detail', args=(self.slug, ))

    def get_config_file_content(self):
        # TODO: Complete the function.
        pass

    def save(self, *args, **kwargs):
        """Override save to make name"""
        now = datetime.now()
        self.name = '%s-%s-%s' % (
            self.baseline, self.product, now.strftime("%Y-%m-%d-%H:%M:%S")
        )
        return super(Build, self).save(*args, **kwargs)

class BuildURL(models.Model):
    type            = models.CharField(verbose_name=_('Name'), max_length=128)
    url             = models.URLField(blank=True, null=True)
    build           = models.ForeignKey(Build)

    def __unicode__(self):
        return self.url
