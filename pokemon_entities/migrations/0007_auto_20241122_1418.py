# Generated by Django 3.1.14 on 2024-11-22 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_pokemon_evolved_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolved_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='evolved_to', to='pokemon_entities.pokemon'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon_entities', to='pokemon_entities.pokemon'),
        ),
    ]
