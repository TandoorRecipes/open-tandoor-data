# Open Tandoor Data

When setting up a new tandoor instance it can be annoying to add all foods, units, supermarkets and categories on your own.
This repository contains community contributed "sensible default" data for these various data objects that can eventually be imported into tandoor. Everything you need to get your recipe collection started.

This is just a starting point. You can still customize and add to these defaults in your own spaces or self-hosted applications.

## Contributing

This project cannot exist without the community maintaining it! Help is much appreciated. 

To help **translate** visit https://translate.tandoor.dev/projects/tandoor-open-data/data/

Contribute **data**

1. Read this readme to understand the core concepts 
2. Go to https://app.tandoor.dev/open-data/ and create yourself an account *
3. Start adding Foods, Conversions and Stores. If you want to do more ask to get verified on discord. 

> *Why do you need an account?: We tried working on the data on GitHub but merging tons of .json files is annoying.
> For that reason we build an editor directly into Tandoor using the [open data plugin](https://github.com/TandoorRecipes/open_data_plugin).
> See the [privacy policy](https://tandoor.dev/privacy/) on tandoor.dev

Data is pulled from tandoor.dev periodically and provided in the defined schema in this repository. 

**Do NOT submit PRs** for data or translations in this repository as there is no way to sync the data back to tandoor.dev.

## Scope

In general only basic objects that are common in many kitchens and for many users should be included in this repository.

For example, a food like `spaghetti` should not be further split into various brands that make them but contain data that is applicable to the average version.

Everything entered should be generally agreed upon by the language you are defining the object in.

If you don't think it's a general thing, maybe try specifying your object a little more. For example don't use pasta when you cannot decide if you want to take the nutritional values of spaghetti or linguine, use the exact kind.

If unsure, ask on discord or leave a comment in the object. 

## Data inheritance

Each object is associated with a `version`. The top level version is `base`. 
Every specific version (e.g. `de`, `fr`) inherits data from the `base` version. 

Specific versions contain data that is only used in certain regions. For example regional foods or regional unit conversions
(mostly packaging sizes) that vary around the world.

The names of all objects in the base version are given in english, all specific objects are in their local language. 

In the future there might be region specific versions like for example `de-DE` or `de-AT`.

## License

The schema in this repository is available under the [Open Database License](https://opendatacommons.org/licenses/odbl/1-0/).
The individual contents of this repository are available under the [Database Contents License](https://opendatacommons.org/licenses/dbcl/1-0/).
