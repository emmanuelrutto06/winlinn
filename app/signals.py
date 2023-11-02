from django.db.models.signals import (
    post_delete,post_init,post_migrate,post_save,
    pre_delete,pre_init,pre_migrate,pre_save
)
from django.core.signals import (
    request_finished,request_started,got_request_exception
)



from django.dispatch import receiver,Signal




######################
# Assignment signals #
######################
counter= Signal(providing_args=[])


######################
# assignment signals #
######################




@receiver(request_finished)
def assignment_request_finished_signal(sender,**kwargs):
    print('this is the assignment request finished signal')

@receiver(request_started)
def assignment_request_started_signal(sender,**kwargs):
    print('this is the assignment request started signal')

@receiver(got_request_exception)
def assignment_got_request_exception_signal(sender,**kwargs):
    print('this is the assignment got request exception signal')


###################
# ChatMessage signals #
###################
counter=Signal(providing_args=[])




################
# ChatMessage signals #
################
@receiver(request_finished)
def chatmessage_request_finished_signal(sender,**kwargs):
    print('this is the chatmessage finished signal')

@receiver(request_started)
def chatmessage_request_started_signal(sender,**kwargs):
    print('this is the chatmessage request started signal')

@receiver(got_request_exception)
def chatmessage_got_request_exception_signal(sender,**kwargs):
    print('this is the chatmessage got request exception signal')



################
# thread signals #
################
counter=Signal(providing_args=[])

################
# thread signals #
################
@receiver(request_finished)
def thread_request_finished_signal(sender,**kwargs):
    print('this is the thread request finished signal')

@receiver(request_started)
def thread_request_started_signal(sender,**kwargs):
    print('this is the thread request started signal')

@receiver(got_request_exception)
def thread_got_request_exception_signal(sender,**kwargs):
    print('this is the thread got request exception signal')


######################
# Membership signals #
######################
counter= Signal(providing_args=[])


######################
# Membership signals #
######################

@receiver(request_finished)
def membership_request_finished_signal(sender,**kwargs):
    print('this is the membership request finished signal')

@receiver(request_started)
def membership_request_started_signal(sender,**kwargs):
    print('this is the membership request started signal')

@receiver(got_request_exception)
def membership_got_request_exception_signal(sender,**kwargs):
    print('this is the membership got request exception signal')


###################
# UserMembership signals #
###################
counter=Signal(providing_args=[])




################
# ChatMessage signals #
################
@receiver(request_finished)
def usermembership_request_finished_signal(sender,**kwargs):
    print('this is the usermembership finished signal')

@receiver(request_started)
def usermembership_request_started_signal(sender,**kwargs):
    print('this is the usermembership request started signal')

@receiver(got_request_exception)
def usermembership_got_request_exception_signal(sender,**kwargs):
    print('this is the usermembership got request exception signal')



################
# Subscription signals #
################
counter=Signal(providing_args=[])

################
# Subscription signals #
################

@receiver(request_finished)
def subscription_request_finished_signal(sender,**kwargs):
    print('this is the subscription request finished signal')

@receiver(request_started)
def subscription_request_started_signal(sender,**kwargs):
    print('this is the subscription request started signal')

@receiver(got_request_exception)
def subscription_got_request_exception_signal(sender,**kwargs):
    print('this is the subscription got request exception signal')


################
# WritersJoin signals #
################
counter=Signal(providing_args=[])

################
# WritersJoin signals #
################

@receiver(request_finished)
def WritersJoin_request_finished_signal(sender,**kwargs):
    print('this is the WritersJoin request finished signal')

@receiver(request_started)
def WritersJoin_request_started_signal(sender,**kwargs):
    print('this is the WritersJoin request started signal')

@receiver(got_request_exception)
def WritersJoin_got_request_exception_signal(sender,**kwargs):
    print('this is the WritersJoin got request exception signal')



################
# Document signals #
################
counter=Signal(providing_args=[])

################
# Document signals #
################
@receiver(request_finished)
def Document_request_finished_signal(sender,**kwargs):
    print('this is the Document request finished signal')

@receiver(request_started)
def Document_request_started_signal(sender,**kwargs):
    print('this is the Document request started signal')

@receiver(got_request_exception)
def Document_got_request_exception_signal(sender,**kwargs):
    print('this is the Document got request exception signal')
