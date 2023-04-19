import os
import traceback
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_DATA = os.path.join(BASE_DIR, "data")
BASE_DIR_LOCALE = os.path.join(BASE_DIR, "locale")
LOG_LEVEL = "DEBUG"


def log(level, msg):
    if LOG_LEVEL.lower() == level.lower():
        print(msg)


def load_data(datatype):
    log("debug", f"loading datatype {datatype}")
    f = open(os.path.join(BASE_DIR_DATA, datatype, "base", "data.json"))
    data = json.loads(f.read())
    return data["data"]


def load_translations(language):
    log("debug", f"loading translations for {language}")
    f = open(os.path.join(BASE_DIR_LOCALE, f"{language}.json"))
    file_data =  f.read()
    if file_data == "":
        return {}
    else:
        data = json.loads(file_data)
        return data


def save_translations(language, data):
    log("debug", f"saving translations for {language}")
    f = open(os.path.join(BASE_DIR_LOCALE, f"{language}.json"), "w")
    f.write(json.dumps(data))


def get_available_translations():
    # TODO load from folder
    return ["de", "en"]


try:
    for l in get_available_translations():
        objects = load_data("food")
        translations = load_translations(l)
        for o in objects:
            if not o["name"] in translations:
                translations[o["name"]] = o["name"]
            if not o["plural_name"] in translations:
                translations[o["plural_name"]] = o["plural_name"]
        save_translations(l, translations)


except Exception as e:
    traceback.print_exc()
    print(f"ERROR failed to load files {e}")
