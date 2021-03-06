# Generated by Django 3.0.5 on 2020-04-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
