# Generated by Django 4.1 on 2022-09-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_asuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asuser',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '正常'), (1, '禁用')], default=0, verbose_name='状态'),
        ),
    ]
