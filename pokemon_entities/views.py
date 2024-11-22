import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    curr_time = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=curr_time,
        disappeared_at__gte=curr_time
        )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemons_on_page = []
    for pokemon in pokemons:
        img_url = request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': img_url,
                'title_ru': pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    if current_pokemon is None:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=current_pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    img_url = request.build_absolute_uri(current_pokemon.image.url)
    pokemon = {
        "title_ru": current_pokemon.title,
        "pokemon_id": pokemon_id,
        "img_url": img_url
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
