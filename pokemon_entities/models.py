from django.utils.timezone import now
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField('Русское название', max_length=200)
    title_en = models.CharField('Английское название', max_length=200, blank=True)
    title_jp = models.CharField('Японское название', max_length=200, blank=True)
    image = models.ImageField('Изображение')
    desciption = models.TextField('Описание', blank=True)
    evolved_from = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='evolved_to',
        verbose_name='Предыдущая эволюция'
    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities'
    )
    lat = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    lon = models.DecimalField('Долгота', max_digits=9, decimal_places=6)
    appeared_at = models.DateTimeField('Время появления', default=now)
    disappeared_at = models.DateTimeField('Время исчезновения', default=now)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
