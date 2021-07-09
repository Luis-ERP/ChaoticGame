# Generated by Django 3.2.5 on 2021-07-01 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulation1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashCard',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simulation1.card')),
                ('type', models.CharField(choices=[('0', 'blue'), ('1', 'green'), ('10', 'yellow'), ('100', 'orange'), ('500', 'purple'), ('1000', 'red'), ('10000', 'black')], max_length=120)),
            ],
            bases=('simulation1.card',),
        ),
    ]
