# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Om titel \xe4ndras kommer urlen fortfarande se ut som gamla titeln.', max_length=200)),
                ('content', models.TextField(help_text='Viss formatering till\xe5ten.  _kursiv_ *fet*, "l\xe4nktext":url.  Tomrad f\xf6r styckesbrytning.')),
                ('posted_time', models.DateTimeField(help_text='L\xe4mna tomt f\xf6r att l\xe4mna posten opublicerad.', null=True, db_index=True, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
                'ordering': ['-posted_time'],
            },
            bases=(models.Model,),
        ),
    ]
