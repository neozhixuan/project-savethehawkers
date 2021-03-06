# Generated by Django 3.2.3 on 2021-10-30 08:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('ordered', models.CharField(blank=True, max_length=1000, null=True)),
                ('stallname', models.CharField(blank=True, max_length=1000, null=True)),
                ('recommend', models.BooleanField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('contributor', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=1000)),
                ('datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Groupbuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stallname', models.CharField(blank=True, max_length=100, null=True)),
                ('destination', models.IntegerField(blank=True, max_length=255, null=True)),
                ('areacollect', models.CharField(blank=True, max_length=1000, null=True)),
                ('contactinfo', models.CharField(blank=True, max_length=1000, null=True)),
                ('additionalinfo', models.CharField(blank=True, max_length=10000, null=True)),
                ('latorigin', models.FloatField(blank=True, max_length=255, null=True)),
                ('longorigin', models.FloatField(blank=True, max_length=255, null=True)),
                ('lat2', models.FloatField(blank=True, max_length=255, null=True)),
                ('long2', models.FloatField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(max_length=255, null=True)),
                ('longtitude', models.FloatField(max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('stalltype', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('hours', models.CharField(blank=True, max_length=300, null=True)),
                ('reco', models.CharField(blank=True, max_length=1000)),
                ('details', models.CharField(blank=True, max_length=10000)),
                ('contributor', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=1000, null=True)),
                ('points', models.IntegerField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=1000, null=True)),
                ('reason', models.CharField(blank=True, max_length=1000, null=True)),
                ('stallname', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal', models.IntegerField(max_length=255, null=True)),
                ('latitude', models.FloatField(max_length=255, null=True)),
                ('longtitude', models.FloatField(max_length=255, null=True)),
                ('searchval', models.CharField(max_length=200)),
                ('blk_no', models.CharField(max_length=255, null=True)),
                ('road_name', models.CharField(max_length=200)),
                ('building', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HawkerStall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(null=True)),
                ('longtitude', models.FloatField(null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('stalltype', models.CharField(blank=True, max_length=255, null=True)),
                ('postalcode', models.IntegerField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('hours', models.CharField(blank=True, max_length=300, null=True)),
                ('reco', models.CharField(blank=True, max_length=1000, null=True)),
                ('details', models.CharField(blank=True, max_length=10000, null=True)),
                ('contributor', models.CharField(blank=True, max_length=1000, null=True)),
                ('image1', models.CharField(blank=True, max_length=2000, null=True)),
                ('image2', models.CharField(blank=True, max_length=2000, null=True)),
                ('image3', models.CharField(blank=True, max_length=2000, null=True)),
                ('image4', models.CharField(blank=True, max_length=2000, null=True)),
                ('image5', models.CharField(blank=True, max_length=2000, null=True)),
                ('message', models.CharField(blank=True, max_length=300, null=True)),
                ('number', models.IntegerField(blank=True, max_length=255, null=True)),
                ('fooddelivery', models.BooleanField(blank=True, null=True)),
                ('phonedelivery', models.BooleanField(blank=True, null=True)),
                ('freelance', models.BooleanField(blank=True, null=True)),
                ('halal', models.BooleanField(blank=True, null=True)),
                ('deals', models.CharField(blank=True, max_length=1000, null=True)),
                ('awards', models.CharField(blank=True, max_length=500, null=True)),
                ('pricerange', models.CharField(blank=True, max_length=1000, null=True)),
                ('facebook', models.CharField(blank=True, max_length=1000, null=True)),
                ('twitter', models.CharField(blank=True, max_length=1000, null=True)),
                ('bookmarks', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(blank=True, null=True, to='project.Comments')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.district')),
                ('email', models.ManyToManyField(blank=True, null=True, to='project.Email')),
                ('menu', models.ManyToManyField(blank=True, null=True, to='project.Menu')),
                ('report', models.ManyToManyField(blank=True, null=True, to='project.Report')),
            ],
        ),
    ]
