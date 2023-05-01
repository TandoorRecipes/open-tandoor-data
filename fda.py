import argparse
import configparser
import json
import os
import sys
from datetime import datetime

import requests as requests

from utils import load_data, save_data

config = configparser.ConfigParser()
config.read("config.ini.template")

api_key = config.get('DEFAULT', "fda_api_key")


def handle_input(default, field_name):
    if isinstance(default, str):
        value = input(f'{field_name} (default:{default}):')
        if value == '':
            value = default

        return value
    else:
        print('select one of the following or enter your own')
        for k in list(default.keys()):
            print(f'{k}) {default[k]}')
        value = input(f'{field_name}:')
        if value.isnumeric():
            value = default[int(value)]

        return value


if not api_key or api_key == '':
    print('missing FDA API key, please copy config.ini.template to config.ini and add your API key')
    sys.exit(1)

food_data = load_data('food')
category_data = load_data('category')
unit_data = load_data('unit')
property_data = load_data('property')

while True:
    os.system('cls')
    fdc_id = input('Please enter FDC id:')
    print(f'loading food {fdc_id} ...')
    response = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={api_key}')
    if response.status_code == 429:
        print('API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information')
        sys.exit(1)

    data = json.loads(response.content)

    food = {
        'slug': '',
        'name': data['description'],
        'plural_name': data['description'],
        'supermarket_category': '',
        'preferred_unit_metric': '',
        'preferred_packaging_unit_metric': '',
        'preferred_unit_imperial': '',
        'preferred_packaging_unit_imperial': '',
        'properties': {
            "food_amount": 100,
            "food_unit": "unit-g",
            "type_values": [],
            "source": f'https://fdc.nal.usda.gov/fdc-app.html#/food-details/{fdc_id}/nutrients'
        },
        'fdc_id': fdc_id,
        'comment': f'FDA import {datetime.now()}'
    }

    print('Please enter field values, just press enter to confirm default')
    while food['slug'] in list(food_data.keys()) or not food['slug'].startswith('food-'):
        print('slug already exists or does not start with food-, please try again')
        food['slug'] = handle_input(f"food-{data['description'].lower().replace(' ', '-').replace(',', '')}", 'slug')

    food['name'] = handle_input(data['description'].lower().replace(',', ''), 'name')
    food['plural_name'] = handle_input(data['description'].lower().replace(',', ''), 'plural name')

    food['supermarket_category'] = handle_input(dict(enumerate([x for x in list(category_data.keys())])), 'supermarket category')
    food['preferred_unit_metric'] = handle_input(dict(enumerate([x for x in list(unit_data.keys())])), 'preferred_unit_metric')
    food['preferred_packaging_unit_metric'] = handle_input(dict(enumerate([x for x in list(unit_data.keys())])), 'preferred_packaging_unit_metric')
    food['preferred_unit_imperial'] = handle_input(dict(enumerate([x for x in list(unit_data.keys())])), 'preferred_unit_imperial')
    food['preferred_packaging_unit_imperial'] = handle_input(dict(enumerate([x for x in list(unit_data.keys())])), 'preferred_packaging_unit_imperial')

    for fn in data['foodNutrients']:
        if fn['nutrient']['id'] == 1008:
            food['properties']['type_values'].append({"property_type": "property-calories", "property_value": round(fn['amount'], 2)})
        if fn['nutrient']['id'] == 1003:
            food['properties']['type_values'].append({"property_type": "property-proteins", "property_value": round(fn['amount'], 2)})
        if fn['nutrient']['id'] == 1005:
            food['properties']['type_values'].append({"property_type": "property-carbohydrates", "property_value": round(fn['amount'], 2)})
        if fn['nutrient']['id'] == 1004:
            food['properties']['type_values'].append({"property_type": "property-fats", "property_value": round(fn['amount'], 2)})

    food_data[food['slug']] = food
    save_data('food', food_data)
