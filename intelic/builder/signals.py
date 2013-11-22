from django.dispatch import Signal

build_added_components = Signal(providing_args=["instance", ])
update_process = Signal(providing_args=["instance", ])
