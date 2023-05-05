import copy
from deepmerge import always_merger

from json import JSONDecodeError
import re
import sys
import traceback
from utils import (
    get_available_datatypes,
    get_available_versions,
    load_data,
    load_schema,
)

errors = []
schema = load_schema()
data = {}


def add_error(language, datatype, object, text):
    if object:
        errors.append(f"({language}-{datatype}) {object}: {text}")
    else:
        errors.append(f"({language}-{datatype}): {text}")


def validate_slugs(l, o, d, schema, base_object):
    for x in list(schema.keys()):
        try:
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
                    if isinstance(i, str):
                        pass  # TODO add validation for strings in lists
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        validate_slugs(l, i, d, schema[x][0], base_object)
            else:
                # validate nested object
                validate_slugs(l, o[x], d, schema[x], base_object)
        except KeyError:
            traceback.print_exc()
            print(o)
            add_error(
                l,
                d,
                base_object,
                f"object is missing key <{x}>",
            )


def validate_schema(l, o, d, schema, base_object):
    for x in list(schema.keys()):
        try:
            if isinstance(schema[x], str):
                if (
                        schema[x].split(":")[0] == "localized_string"
                        or schema[x].split(":")[0] == "string"
                ):
                    if not re.fullmatch(r"([A-z0-9\-\(\)\&\s])+", o[x]):
                        add_error(
                            l,
                            d,
                            base_object,
                            f"<{o[x]}> contains invalid characters (only A-z,0-9,-,(,),& and whitespace allowed) - feel like it should be allowed? please open an issue on github",
                        )
                    if len(o[x]) > int(schema[x].split(":")[1]):
                        add_error(
                            l,
                            d,
                            base_object,
                            f"<{o[x]}> exceeded lenght for field <{x}>",
                        )
                if schema[x].split(":")[0] == "number":
                    if not (isinstance(o[x], int) or isinstance(o[x], float)):
                        add_error(l, d, base_object, f"{o[x]} is not a number")
                if schema[x].split(":")[0] == "options":
                    if not o[x] in schema[x].split(":")[1:]:
                        add_error(
                            l,
                            d,
                            base_object,
                            f"invalid choice <{o[x]}> for field <{x}> valid options are: {', '.join(schema[x].split(':')[1:])}",
                        )
                if x == "source":
                    if schema[x] == "required":
                        if not "source" in o:
                            add_error(
                                l,
                                d,
                                base_object,
                                "object is  missing mandatory source attribute",
                            )
                        elif o["source"].strip() == "":
                            add_error(
                                l,
                                d,
                                base_object,
                                "object mandatory source is empty",
                            )
                if schema[x] == "slug":
                    if not o[x].startswith(f"{d}-"):
                        add_error(
                            l,
                            d,
                            base_object,
                            f"slug field needs to start with <{d}->",
                        )
            elif isinstance(schema[x], list):
                for i in o[x]:
                    if isinstance(schema[x][0], str):
                        if schema[x][0].split(":")[0] == "reference":
                            if not i in data[l][schema[x][0].split(":")[1]]["keys"]:
                                add_error(
                                    l,
                                    d,
                                    base_object,
                                    f'could not find reference <{i}> in list for datatype <{schema[x][0].split(":")[1]}>',
                                )
                    else:
                        # lists can only contain objects of the same type. validate all list entries against the first type in schema.
                        validate_schema(l, i, d, schema[x][0], base_object)
            else:
                # validate nested object
                validate_schema(l, o[x], d, schema[x], base_object)
        except KeyError:
            pass  # handled in validate_slugs


def validate_slug_characters(language, datatype, slug):
    if not re.fullmatch(r"(([a-z1-9])+(\-)*)+", slug):
        add_error(
            language,
            datatype,
            slug,
            "Slugs can only contain lower case characters and numbers connected with -",
        )


for l in ["base"] + get_available_versions():
    data[l] = {}
    for d in get_available_datatypes():
        data[l][d] = {
            "keys": [],
            "names": [],
            "fdc_ids": [],
            "data": {},
        }
        try:
            version_data = always_merger.merge(load_data(d, l), data["base"][d]["data"])
            for k in list(version_data.keys()):  # TODO prevent errors from showing for each language
                if k in data[l][d]["keys"]:
                    add_error(l, d, k, "Duplicate key, object ignored")
                else:
                    data[l][d]["keys"].append(k)
                    data[l][d]["data"][k] = version_data[k]
                if d in ['food']:
                    fdc_id = data[l][d]["data"][k]['fdc_id']
                    if fdc_id in data[l][d]["fdc_ids"]:
                        add_error(l, d, k, f"Duplicate FDC ID {fdc_id}")
                    else:
                        data[l][d]["fdc_ids"].append(fdc_id)
                if d in ['food', 'unit', 'property', 'category', 'supermarket']:
                    name = data[l][d]["data"][k]['name']
                    if name in data[l][d]["names"]:
                        add_error(l, d, k, f"Duplicate name {name}")
                    else:
                        data[l][d]["names"].append(name)
        except JSONDecodeError as e:
            add_error(
                l, d, None, f"JSON format error: {e.msg} on line {e.lineno}:{e.colno}"
            )

for l in ["base"] + get_available_versions():
    for d in get_available_datatypes():
        try:
            version_data = load_data(d, l)
            if l != "base":
                version_data = always_merger.merge(load_data(d, l), data["base"][d]["data"])
            for k in list(version_data.keys()):
                o = version_data[k]
                validate_slugs(l, o, d, schema[d], k)
                validate_schema(l, o, d, schema[d], k)
                validate_slug_characters(l, d, k)
        except JSONDecodeError as e:
            pass

print("========================================")
if len(errors) > 0:
    print(f"FOUND {len(errors)} errors")
    for e in errors:
        print(e)
    print("========================================")
    sys.exit(1)
else:
    print("All files validated without errors")
    print("========================================")
    sys.exit(0)
