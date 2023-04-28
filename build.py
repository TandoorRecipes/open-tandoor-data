from deepmerge import always_merger

from utils import load_data, get_available_versions, get_available_datatypes, load_translations, load_schema, save_build_version

global_schema = load_schema()


def recursive_translate_object(l, d, o, schema, lt):
    for x in list(schema.keys()):
        try:
            if isinstance(schema[x], str):
                if schema[x].split(":")[0] == "localized_string":
                    if o[x] in lt:
                        o[x] = lt[o[x]]
                    else:
                        o['missing_translation'] = True
            elif isinstance(schema[x], list):
                print(schema[x], o)
                for i in o[x]:
                    if isinstance(i, str):
                        pass  # TODO add validation for strings in lists
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        o[x] = recursive_translate_object(l, d, i, schema[x][0], lt)
            else:
                # validate nested object
                o[x] = recursive_translate_object(l,  d, o[x], schema[x], lt)
        except KeyError:
            print('key error')

    return o


language_data = {
    'metadata': {}
}

for l in get_available_versions():
    language_data[l] = {}
    language_translations = load_translations(l)
    for d in get_available_datatypes():
        base_data = load_data(d, 'base')
        language_data[l][d] = {}
        version_data = always_merger.merge(load_data(d, l), base_data)
        for k in list(version_data.keys()):
            translated_object =  recursive_translate_object(l, d, version_data[k], global_schema[d], language_translations)
            # TODO always use specifc ones as they dont need translation
            if not 'missing_translation' in translated_object: # TODO recursive check or base object set
                language_data[l][d][k] = translated_object

    save_build_version(l, language_data[l])

print(language_data)