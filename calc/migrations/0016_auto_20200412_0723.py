# Generated by Django 3.0.2 on 2020-04-12 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0015_auto_20200331_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marriage',
            name='female',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='female', to='calc.Person'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='male',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='male', to='calc.Person'),
        ),
    ]