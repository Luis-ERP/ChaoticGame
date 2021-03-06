# Generated by Django 3.2.5 on 2021-07-01 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dungeon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('0', 'light'), ('1', 'dark'), ('2', 'fire'), ('3', 'water'), ('4', 'earth'), ('5', 'air')], max_length=120)),
                ('attack1', models.IntegerField()),
                ('defense1', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField()),
                ('cash', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('name', models.CharField(max_length=140)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='simulation1.player')),
            ],
        ),
        migrations.CreateModel(
            name='HeroCard',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simulation1.card')),
                ('level', models.IntegerField()),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='simulation1.hero')),
            ],
            bases=('simulation1.card',),
        ),
        migrations.CreateModel(
            name='DungeonCard',
            fields=[
                ('card_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='simulation1.card')),
                ('dungeon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='simulation1.dungeon')),
            ],
            bases=('simulation1.card',),
        ),
    ]
