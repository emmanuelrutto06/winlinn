from django.db import migrations
from django.contrib.auth.models import User
from authentication.models import UserManager, Adminstration
from django.contrib.auth.hashers import make_password

def default_site_config(apps, schema_editor):
    """ Default site configurations """

    User = apps.get_model('authentication', 'User')
    user_password = make_password('123456')
    id_val ='1'
  

    User = apps.get_model('authentication', 'User')
    User.objects.bulk_create([
        User(
                first_name ='python',
                last_name='python',
                username='python',
                password =user_password,
                email ='admin@gmail.com',
                is_active =True,
                is_client =False,
                is_administrator =False,
                is_superuser =True,
                is_staff =True,
                date_of_birth='1990-01-01',
                phone='+254710737392',
                additional_phone='+254710737392',
                time_zone ='UTC',
                night_calls =True,

               ),
    ])



class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_site_config),
    ]
