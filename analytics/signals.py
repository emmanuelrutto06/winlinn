# https://kirr.co/mh9shf
from django.dispatch import Signal
object_viewed_signal = Signal(providing_args=['instance','request'])

