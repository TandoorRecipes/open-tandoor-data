import os
import traceback
import json

from utils import (
    get_available_translations,
    load_data,
    load_translations,
    save_translations,
)


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
