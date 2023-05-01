import argparse
import configparser
import json
import sys

import requests as requests

from utils import load_data, save_data

config = configparser.ConfigParser()
config.read("config.ini.template")

api_key = config.get('DEFAULT', "fda_api_key")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", '--food', help="fdc database id of a food", action="append")

    return parser.parse_args()


args = parse_args()

if not args.food:
    print('missing food ids')
    sys.exit(1)

if not api_key or api_key == '':
    print('missing FDA API key, please copy config.ini.template to config.ini and add your API key')
    sys.exit(1)

food_data = load_data('food')




for fdc_id in args.food:
    print(f'loading food {fdc_id} ...')
    response = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={api_key}')
    if response.status_code == 429:
        print('API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information')
        sys.exit(1)

    data = json.loads(response.content)

    print('Please enter field values, just press enter to confirm default')
    slug_default = data['description'].lower().replace(' ', '-').replace(',', '')
    slug = input(f'slug (default:{slug_default}):')
    if slug == '':
        slug = slug_default

    food = {
        'slug': slug,
        'name': data['description'],
        'plural_name': data['description'],
        'supermarket_category': '',
        'preferred_unit_metric': '',
        'preferred_packaging_unit_metric': '',
        'preferred_unit_imperial': '',
        'preferred_packaging_unit_imperial': '',
        'properties': {},
        'fdc_id': fdc_id
    }
    food_data[slug] = food
    save_data('food', food_data)
