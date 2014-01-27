from django.dispatch import Signal
from django.db.models.signals import *

build_added_components = Signal(providing_args=["instance", ])
update_process = Signal(providing_args=["instance", ])
pre_patches_package_create = Signal(providing_args=["instance", ])
post_patches_package_create = Signal(providing_args=["instance", "patches_package" ])
