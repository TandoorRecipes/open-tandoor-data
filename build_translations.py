import os
import traceback
import json

from utils import (
    get_available_versions,
    load_data,
    load_translations,
    save_translations, get_available_datatypes, load_schema,
)


def find_localized_strings(o, schema):
    localized_strings = []
    for x in list(schema.keys()):
        try:
            if isinstance(schema[x], str):
                if schema[x].split(":")[0] == "localized_string":
                    localized_strings.append(o[x])
            elif isinstance(schema[x], list):
                for i in o[x]:
                    if isinstance(i, str):
                        pass  # TODO check for localized strings in lists
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        localized_strings += find_localized_strings(i, schema[x][0])
            else:
                # validate nested object
                localized_strings += find_localized_strings(o[x], schema[x])
        except KeyError:
            print('key error')

    return localized_strings


global_schema = load_schema()
try:
    translations = load_translations('en')
    for d in get_available_datatypes():
        base_data = load_data(d, 'base')

        for k in list(base_data.keys()):
            translation_strings = find_localized_strings(base_data[k], global_schema[d])
            for t in translation_strings:
                if t not in translations:
                    translations[t] = t

    save_translations('en', translations)


except Exception as e:
    traceback.print_exc()
    print(f"ERROR failed to load files {e}")
