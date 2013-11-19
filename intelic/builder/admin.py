from django.contrib import admin

import models, forms

# ##################################################
# Inlines
# ##################################################

class JobURLInline(admin.StackedInline):
    model = models.JobURL
    extra = 1

# ##################################################
# Admins
# ##################################################


class BaselineAdmin(admin.ModelAdmin):
    list_display = ('name', 'git_repo', 'is_active')
    search_fields = ('name', )
    fields = ('name', 'git_repo')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'git_repo', 'is_active')
    list_filter = ('form_class', )
    search_fields = ('name', )
    filter_horizontal = ('baseline', )
    fields = ('name', 'form_class', 'git_repo', 'baseline')

class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    fields = ('name', )

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'git_repo', 'is_active')
    list_filter = ('type', )
    filter_horizontal = ('baseline', 'product')
    fields = ('name', 'type', 'source', 'git_repo', 'baseline', 'product')

class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'baseline', 'product', 'created_at')
    list_filter = ('baseline', 'product')
    search_fields = ('name', )
    inlines = (
        JobURLInline,
    )

admin.site.register(models.Baseline, BaselineAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ComponentType, ComponentTypeAdmin)
admin.site.register(models.Component, ComponentAdmin)
admin.site.register(models.Job, JobAdmin)
