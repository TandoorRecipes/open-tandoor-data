# validate json format
# validate all slugs link to existing entries -> test
# validate uniqueness of slugs -> test
# validate typed fileds (numbers, strings and selectable options e.g. base units, types, ...)
# slug field allowed characters (no whitespace, only lower case, only dash)
# validate no special characters in localized fields ??
# validate all files needed for langauge exist ? (or do we not want to enforce this?)

import sys
from utils import (
    get_available_datatypes,
    get_available_translations,
    load_data,
    load_schema,
)

errors = []
schema = load_schema()
data = {}


def add_error(language, datatype, object, text):
    errors.append(f"({language}-{datatype}) {object}: {text}")


def validate_slugs(l, o, d, schema, base_object):
    for x in list(schema.keys()):
        if isinstance(schema[x], str):
            if schema[x].split(":")[0] == "reference":
                if not o[x] in data[l][schema[x].split(":")[1]]["keys"]:
                    add_error(
                        l,
                        d,
                        base_object,
                        f'could not find reference <{o[x]}> for datatype <{schema[x].split(":")[1]}>',
                    )
        elif isinstance(schema[x], list):
            for i in o[x]:
                # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                validate_slugs(l, i, d, schema[x][0], base_object)
        else:
            # validate nested object
            validate_slugs(l, o[x], d, schema[x], base_object)


def validate_slug_characters(language,datatype,object):
    pass

for l in get_available_translations():
    data[l] = {}
    for d in get_available_datatypes():
        data[l][d] = {
            "keys": [],
            "data": [],
        }
        for o in load_data(d, l):
            if o["slug"] in data[l][d]["keys"]:
                add_error(l, d, o["slug"], "Duplicate key")
            else:
                data[l][d]["keys"].append(o["slug"])
            data[l][d]["data"].append(o)  # TODO merge down


for l in get_available_translations():
    for d in get_available_datatypes():
        for o in load_data(d, l):
            validate_slugs(l, o, d, schema[d], o["slug"])


print("========================================")
if len(errors) > 0:
    print(f"FOUND {len(errors)} errors")
    for e in errors:
        print(e)
    print("========================================")
    sys.exit(1)
else:
    print('All files validated without errors')
    print("========================================")
    sys.exit(0)