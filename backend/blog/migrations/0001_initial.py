# Generated by Django 2.0.2 on 2018-03-04 01:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.CharField(max_length=128)),
                ('format', models.CharField(max_length=4)),
                ('datetime', models.DateTimeField()),
                ('content', models.TextField()),
            ],
        ),
    ]
