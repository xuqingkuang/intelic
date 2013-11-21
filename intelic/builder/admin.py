from django.contrib import admin

import models, forms

# ##################################################
# Admins
# ##################################################

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('form_class', )
    search_fields = ('name', )
    fields = ('name', 'desc', 'form_class')


class BaselineAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', )
    filter_horizontal = ('product', )
    fields = ('name', 'product', 'desc')

class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    fields = ('name', )

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_active')
    list_filter = ('type', )
    filter_horizontal = ('baseline', 'product')
    fields = ('name', 'desc', 'type', 'source', 'baseline', 'product', 'gerrit_url')

class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'baseline', 'product', 'created_at')
    list_filter = ('baseline', 'product')
    search_fields = ('name', )

admin.site.register(models.Baseline, BaselineAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ComponentType, ComponentTypeAdmin)
admin.site.register(models.Component, ComponentAdmin)
admin.site.register(models.Build, BuildAdmin)
