# Generated by Django 2.0.2 on 2018-03-07 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=64)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blog.BlogPost')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='blogtag',
            unique_together={('post', 'tag')},
        ),
    ]
