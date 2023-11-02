from django.contrib.auth.models import Permission,Group,User
from django.contrib.contenttypes.models import ContentType


#################
# set content types 
user_content_type=ContentType.objects.get_for_model(User)
##################
# create permissions

#################
can_view_uploaded_files=Permission.objects.create(
    codename='can_view_uploaded_files',
    name='can view uploaded files',
    content_type=user_content_type
)
can_approve_orders_completed=Permission.objects.create(
    codename='can_approve_orders_completed',
    name='can approve orders completed',
    content_type=user_content_type
)
can_return_order_revision=Permission.objects.create(
    codename='can_return_orders_revision',
    name='can return orders revision',
    content_type=user_content_type
)

can_edit_deadlines=Permission.objects.create(
    codename='can_edit_deadlines',
    name='can edit deadlines',
    content_type=user_content_type
)

can_view_payment_details=Permission.objects.create(
    codename='can_view_payment_details',
    name='can view payment details',
    content_type=user_content_type
)


can_assign_orders=Permission.objects.create(
    codename='can_assign_orders',
    name='can assign orders',
    content_type=user_content_type
)

can_issue_quote=Permission.objects.create(
    codename='can_issue_quotes',
    name='can issue quotes',
    content_type=user_content_type
)


# set groups into permissions

##############
# create groups
client_group,created = Group.objects.get_or_create(name='clients_group')
writers_group,created = Group.objects.get_or_create(name='writers_group')
support_group,created = Group.objects.get_or_create(name='support_group')

#################
# assign permissions to groups

client_group.permissions.add(
    can_approve_orders_completed,
    can_return_order_revision
)
support_group.permissions.add(
    can_assign_orders,can_issue_quote,
    can_return_order_revision,can_approve_orders_completed,
    can_edit_deadlines
)