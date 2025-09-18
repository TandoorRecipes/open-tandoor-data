import json
import os
import sys

import requests

from utils import save_data

TANDOOR_API_KEY = os.getenv('TANDOOR_API_KEY', '')
REQUEST_HEADERS = {
    'Authorization': f'Bearer {TANDOOR_API_KEY}'
}

ENDPOINTS = [
    'open-data-unit',
    'open-data-property',
    'open-data-category',
    'open-data-store',
    'open-data-food',
    'open-data-conversion',
]


def get_unit_object(e):
    return {
        'name': e['name'],
        'plural_name': e['plural_name'],
        'type': e['type'],
        'base_unit': e['base_unit'],
        'comment': e['comment'],
    }


def get_property_object(e):
    return {
        'name': e['name'],
        'unit': e['unit'],
        'fdc_id': e['fdc_id'],
        'comment': e['comment'],
    }


def get_category_object(e):
    return {
        'name': e['name'],
        'comment': e['comment'],
    }


def get_food_object(e):
    properties = {
        'food_amount': e['properties_food_amount'],
        'food_unit': e['properties_food_unit']['slug'],
        'source': e['properties_source'],
        'type_values': [],
    }
    for p in e['properties']:
        properties['type_values'].append({
            'property_type': p['property']['slug'],
            'property_value': p['property_amount'],
        })

    return {
        'name': e['name'],
        'plural_name': e['plural_name'],
        'store_category': e['store_category']['slug'],
        # 'preferred_unit_metric': e['preferred_unit_metric']['slug'],
        # 'preferred_packaging_unit_metric': e['preferred_shopping_unit_metric']['slug'],
        # 'preferred_unit_imperial': e['preferred_unit_imperial']['slug'],
        # 'preferred_packaging_unit_imperial': e['preferred_shopping_unit_imperial']['slug'],
        'properties': properties,
        'fdc_id': e['fdc_id'],
        'comment': e['comment'],
    }


def get_conversion_object(e):
    return {
        'food': e['food']['slug'],
        'base_amount': e['base_amount'],
        'base_unit': e['base_unit']['slug'],
        'converted_amount': e['converted_amount'],
        'converted_unit': e['converted_unit']['slug'],
        'source': e['source'],
        'comment': e['comment'],
    }


def get_store_object(e):
    categories = []
    for c in e['category_to_store']:
        categories.append(c['category']['slug'])
    return {
        'name': e['name'],
        'categories': categories,
        'comment': e['comment'],
    }


def update_data():
    for endpoint in ENDPOINTS:
        object_type = endpoint.replace('open-data-', '')
        response = requests.get(f'https://app.tandoor.dev/api/{endpoint}/', headers=REQUEST_HEADERS)
        type_data = {}
        json_response = json.loads(response.content)
        for e in json_response['results']:
            version = e['version']['code']
            if version not in type_data:
                type_data[version] = {'data': {}}

            parsed_object = None
            if object_type == 'unit':
                parsed_object = get_unit_object(e)
            if object_type == 'property':
                parsed_object = get_property_object(e)
            if object_type == 'category':
                parsed_object = get_category_object(e)
            if object_type == 'store':
                parsed_object = get_store_object(e)
            if object_type == 'food':
                parsed_object = get_food_object(e)
            if object_type == 'conversion':
                parsed_object = get_conversion_object(e)

            type_data[version]['data'][e['slug']] = parsed_object
        for v in list(type_data.keys()):
            save_data(object_type, type_data[v]['data'], language=v)


if TANDOOR_API_KEY == '':
    print('Missing Tandoor API Key')
    sys.exit(1)

update_data()
