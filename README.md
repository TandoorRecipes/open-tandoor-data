# Open Tandoor Data
This repository contains community contributed data about various data objects that you need for your recipe collection. 

**WIP** This repository currently just contains a work in progress concept of how this database could be structured. 

## Data inheritance
Certain parts of this dataset are universal to all languages/cultures while others are individual. To prevent duplicate data while also allowing unique culture or language specific aspects data in this repository is best consumed while inheriting base data. It is also possible to split data into multiple chunks so consumers can choose to only consume parts of it. 

When consuming data in the example below the consumer would first load the `data.json` included in the base directory. After that it will load the data of a specific language/culture. Anything in the specific file will override the base file. This could also be layered to allow multi stage inheritance. 

Labels and text contained in the `base` version are **always** given in english. Data locale specific folders are given in their respective languages. 

```
data
  food
    base
      data.json
    de
      data.json
    en
      data.json
    ...
  unit
    ...
  supermarket_category
    ...
  supermarket
    ...
  alias
    ...
```

## Datatypes
This repository contains different datatypes which have the following schema. 

All objects in each nesting depth can have the attribute `comment` or `comment_*` which should not 
be consumed by any parser and allows adding editor notes to objects. 

All fields markt as strings should not be longer than 128 characters.

### Food
Food is the central data object which has relations to almost every other object.
```json
[
	{
	  "slug": "<unique_food_slug>",
	  "name": "<food_name>",
	  "plural_name": "<food_plural_name>",
	  "description" : "<food_description>",
	  "supermarket_category": "<category_slug>",
	  "preferred_unit": "<unit_slug>",
	  "preferred_packaging_unit": "<unit_slug>",
	  "properties": {
		  "food_amount": "<food_amount>",
	      "food_unit": "<unit_slug>",
		  "type_values": [
			{
				"property_type": "<property_slug>",
				"property_value": "<property_value>",
			},
			...
		],
	  },
	  "fdc_id": "<usda_database_fdc_id>"
	},
	...
]
```

- [string] `name`: common food name. Should be as generic as possible while identifying a food precicely. Should not include brand names. 
- (optional) [string] `plural_name`: Plural name of a food
- (optional) [text] `description`: Description of the food for the end user. 
- (optional) [slug] `supermarket_category`: Slug of a supermarket category
- (optional) [slug] `preferred_unit`: Slug of a unit, typically used unit for a food in recipes
- (optional) [slug] `preferred_packaging_unit`: Slug of a unit, typically used as a packaging unit in shopping or stock keeping.
- (optional) [object] `properties`: properties of a food (nutritions, allergens, ...)
  - [number] `food_amount`: base amount property values are given for
  - [slug] `food_unit`: Unit slug of unit measuring the food_amount
  - [array] `typed_values`: Array of property type/value pairs:
    - [slug] `property_type`: Slug of property type
    - [number] `property_value`: Value of the property
- (optional) [text] `fdc_id`: Food data can be sourced from the [USDA Database](https://fdc.nal.usda.gov/fdc-app.html#/) which also contains the FDC ID


### Unit
Units of measurement. The `base_unit` is optional and can tell tandoor which standardized unit it is (e.g. g, kg, pound, fl.oz.). This allows automatic unit conversion while still allowing the user the freedom to choose how a unit should be displayed (e.g. gram, Gram, g, ...)

```json
[
	{
	  "slug": "<unique_unit_slug>",
	  "name": "<unit_name>",
	  "plural_name": "<unit_plural_name>",
	  "base_unit": "<base_unit>",
	  "type": "volume|weight|other",
	  "description" : "<unit_description>"
	},
	...
]
```

### Property
Food properties. This can be nutrition types, allergens, CO2 footprints or whatever the user wants. The standard database should only include nutritions and maybe allergenes. 

```json
[
	{
	  "slug": "<unique_property_slug>",
	  "name": "<property_name>",
	  "unit": "<property_unit>",
	  "description" : "<property_description>"
	},
	...
]
```

### Category
Category of food in a typical supermarket. Allows automatic sorting.
```json
[
	{
	  "slug": "<unique_category_slug>",
	  "name": "<category_name>",
	},
	...
]
```

### Supermarket
Supermarkets contain data about available categories of foods and their order in a typical store of that kind.

Since even stores of a single brand often differ from location to location this might not be all that useful although it could act as a starting point for users to just slightly modify in order to adapt to their preferred stores. 

```json
[
	{
	  "slug": "<unique_supermarket_slug>",
	  "categories" : [
		  "<category_slug>",
		  ...
	  ],
	},
	...
]
```

### Alias

Often Foods or Units have different names or different ways of writing them. This datatype allows to define common aliases so automatic matching systems can apply these aliases to keep data quality high. Most of these aliases are likely language specific. 

```json
[
	{
	  "target_object": "<object_slug>",
	  "type": "<unit|food>",
	  "pattern": [
		"<regex_matching_pattern>",
		...
	  ]
	},
	...
]
```


### Unit Conversions

Tandoor can by default convert between all common weight and all common volume units. Converting from weight to unit and vice versa requires custom conversions as this is differnt for each food. Also there are often packaging units (pack, jar, pcs, ...) that convert differently for each food. 

```json
[
	{
		"food" : "<food_slug>",
		"base_amount" : "<base_amount>",
		"base_unit" : "<unit_slug>",
		"converted_amount" : "<converted_amount>",
		"converted_unit" : "<unit_slug>",
	},
	...
]
```

## Contributing
Currently this dataset is in a design phase and content contributions will not be accepted.
Once finalized contributions trough pull requests are welcome. These requests will then be merged by maintainers of the individual modules (see CONTRIBUTERS.md)

## License

The license has not yet been choosen, options include
https://opendatacommons.org/licenses/odbl/1-0/ 
https://opendatacommons.org/licenses/dbcl/1-0/
AGPL
MIT
...
