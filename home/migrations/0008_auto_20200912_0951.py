# Generated by Django 3.1.1 on 2020-09-12 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200912_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapinfo',
            name='content',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
