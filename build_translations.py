import os
import traceback
import json

from utils import (
    get_available_versions,
    load_data,
    load_translations,
    save_translations, get_available_datatypes, load_schema,
)


def find_localized_strings(l, d, o, schema):
    localized_strings = []
    for x in list(schema.keys()):
        try:
            if isinstance(schema[x], str):
                if schema[x].split(":")[0] == "localized_string":
                    localized_strings.append(o[x])
            elif isinstance(schema[x], list):
                for i in o[x]:
                    if isinstance(i, str):
                        pass  # TODO add validation for strings in lists
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        localized_strings += find_localized_strings(l, d, i, schema[x][0])
            else:
                # validate nested object
                localized_strings += find_localized_strings(l, d, o[x], schema[x])
        except KeyError:
            print('key error')

    return localized_strings


global_schema = load_schema()
try:
    for l in get_available_versions():
        translations = load_translations(l)
        for d in get_available_datatypes():
            version_data = load_data(d)

            for k in list(version_data.keys()):
                translation_strings = find_localized_strings(l, d, version_data[k], global_schema[d])
                for t in translation_strings:
                    if not t in translations:
                        translations[t] = t

        save_translations(l, translations)


except Exception as e:
    traceback.print_exc()
    print(f"ERROR failed to load files {e}")
