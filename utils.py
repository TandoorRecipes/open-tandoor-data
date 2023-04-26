import os
import traceback
import json
from glob import glob


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_DATA = os.path.join(BASE_DIR, "data")
BASE_DIR_LOCALE = os.path.join(BASE_DIR, "locale")
LOG_LEVEL = "NONE"


def log(level, msg):
    if LOG_LEVEL.lower() == level.lower():
        print(msg)


def load_data(datatype, language="base"):
    log("debug", f"loading datatype {datatype}")

    try:
        f = open(
            os.path.join(BASE_DIR_DATA, datatype, language, "data.json"),
            encoding="UTF-8",
        )
        data = json.loads(f.read())
        return data["data"]
    except FileNotFoundError:
        log("debug", f"no data found for {datatype} in version {language}")
        return []



def load_schema():
    log("debug", f"loading schema")

    f = open(
        os.path.join(BASE_DIR, "schema.json"),
        encoding="UTF-8",
    )
    return json.loads(f.read())


def load_translations(language):
    log("debug", f"loading translations for {language}")
    f = open(os.path.join(BASE_DIR_LOCALE, f"{language}.json"), encoding="UTF-8")
    file_data = f.read()
    if file_data == "":
        return {}
    else:
        data = json.loads(file_data)
        return data


def save_translations(language, data):
    log("debug", f"saving translations for {language}")
    f = open(os.path.join(BASE_DIR_LOCALE, f"{language}.json"), "w", encoding="UTF-8")
    f.write(json.dumps(data))


def get_available_versions():
    versions = []
    schema = load_schema()
    for s in list(schema.keys()):
        for f in os.scandir(os.path.join(BASE_DIR_DATA, s)):
            if f.is_dir():
                if not f.name in versions and not f.name == "base":
                    versions.append(f.name)
    return versions


def get_available_datatypes():
    schema = load_schema()
    return list(schema.keys())
