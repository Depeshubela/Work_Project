# Generated by Django 4.0.8 on 2022-11-28 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0018_genre_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='genre_name',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True, default='', max_length=999, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='function.genre'),
        ),
    ]
