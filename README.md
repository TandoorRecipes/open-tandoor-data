# Open Tandoor Data

When setting up a new tandoor instance it can be annoying to add all foods, units, supermarkets and categories on your own.
This repository contains community contributed "sensible default" data for these various data objects that can eventually be imported into tandoor. Everything you need to get your recipe collection started.

This is just a starting point. You can can still customize and add to these defaults in your own spaces or self-hosted applications.

## Scope

In general only basic objects that are common in many kitchens and for many users should be included in this repository.

For example, a food like `spaghetti` should not be further split into various brands that make them but contain data that is applicable to the average version.

Everything entered should be generally agreed upon by the language you are defining the object in.

If you don't think it's a general thing, maybe try specifying your object a little more. For example don't use pasta when you cannot decide if you want to take the nutritional values of spaghetti or linguine, use the exact kind.

If unsure, note this in your PR and let another person decide with you.

## Data inheritance

Certain parts of this dataset are universal to all languages/cultures while others are individual. To prevent duplicate data while also allowing unique culture or language specific aspects data in this repository is best consumed while inheriting base data.

The order is

1. base
2. language code (e.g. `de`, `pt`)
3. language and country code (e.g. `de-de`, `de-ch`)

When consuming data the consumer would first load the `data.json` included in the base directory. After that it will load the data of a specific language and possibly country afterwards. Anything found in a more specific version will override the more basic version.

Labels and text contained in the `base` version are **always** given in english. Data in locale specific folders are given in their respective languages.

```
data
  food
    base
      data.json
    de
      data.json
    de-de
      data.json
	en
	  data.json
    ...
  unit
    ...


```

## Data types

This repository contains different data types which are defined in schema.json

<!-- Until this is created automatically, I really think it makes sense to give a short overview of the data types -->

### Food

This is the most important data type for tandoor. Together with an amount and a unit it forms the ingredient used in a recipe. We want to include basic foods that can be found in many users' kitchens.

### Unit

This refers to the unit that a food can come in. This means metric units such as grams, kilograms, and liters or standard units such as pounds, cups, and quarts.

### Category

These are the categories used by the shopping list.

<!-- Include rationale behind the categories that make up this collection of data. E.g. why was dairy included but not cheese? -->

### Property

### Store (Supermarket)

Stores can contain one or more categories, letting users sort and filter their shopping lists.

### Conversion

An upcoming feature will let you automatically convert units to make it easier to import and harmonize recipes (for instance, to always use metric units instead of imperial). When converting from volumetric measures to weight, the individual density of the food is crucial. These individual conversion rates are stored in this data type.

### Comments

All objects in each nesting depth can have the attribute `comment` or `comment_*` which should not
be consumed by any parser and allows adding editor notes to objects.

### Sources

Certain objects enforce stating sources for information. This should make it easier to validate information later.
Most times only one `source` attribute is enforced.
If multiple sources should be given you can use `source_1`,`source_2`, ...

Sources should be urls if possible or otherwise plausible descriptions of how data was obtained.

## Contributing

Feel free to contribute to this repository.

1. Fork it
2. Edit whatever file you want
3. Submit a PR. If applicable, describe which decisions might need to be reviewed in particular.

## License

The schema in this repository is available under the [Open Database License](https://opendatacommons.org/licenses/odbl/1-0/).
The individual contents of this repository are available under the [Database Contents License](https://opendatacommons.org/licenses/dbcl/1-0/).
