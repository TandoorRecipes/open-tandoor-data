from deepmerge import always_merger

from utils import load_data, get_available_versions, get_available_datatypes, load_translations, load_schema, save_build_version

global_schema = load_schema()


def recursive_translate_object(l, d, o, schema, lt):
    obj_mt = False
    for x in list(schema.keys()):
        try:
            if isinstance(schema[x], str):
                if schema[x].split(":")[0] == "localized_string":
                    if o[x] in lt:
                        o[x] = lt[o[x]]
                    else:
                        obj_mt = True
            elif isinstance(schema[x], list):
                for i in o[x]:
                    if isinstance(i, str):
                        pass  # TODO add translation for strings in lists
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        o[x], mt = recursive_translate_object(l, d, i, schema[x][0], lt)
                        obj_mt = obj_mt or mt
            else:
                # validate nested object
                o[x], mt = recursive_translate_object(l, d, o[x], schema[x], lt)
                obj_mt = obj_mt or mt
        except KeyError:
            print('key error')

    return o, obj_mt


# TODO add more metadata to build files for display in applications
language_data = {
    'metadata': {
        'versions': get_available_versions(),
        'datatypes': get_available_datatypes(),
    }
}

for l in get_available_versions():
    language_data[l] = {
        'metadata': {}
    }
    language_data['metadata'][l] = {}
    language_translations = load_translations(l)
    for d in get_available_datatypes():
        base_data = load_data(d, 'base')
        localized_base_data = {}

        for k in list(base_data.keys()):
            translated_object, missing_translation = recursive_translate_object(l, d, base_data[k], global_schema[d], language_translations)
            if not missing_translation:
                localized_base_data[k] = translated_object

        language_data[l][d] = always_merger.merge(load_data(d, l), localized_base_data)

        language_data['metadata'][l][d] = len(list(language_data[l][d].keys()))

    save_build_version(l, language_data[l])

save_build_version('meta', language_data['metadata'])
