from django.dispatch import Signal

build_added_components = Signal(providing_args=["instance", ])
