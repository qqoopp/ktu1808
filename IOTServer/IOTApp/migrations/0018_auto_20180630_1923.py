# Generated by Django 2.0.5 on 2018-06-30 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IOTApp', '0017_auto_20180603_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tdevice',
            name='StatusCd',
            field=models.CharField(choices=[('ON', 'On'), ('OFF', 'Off')], max_length=3, null=True, verbose_name='Status'),
        ),
    ]