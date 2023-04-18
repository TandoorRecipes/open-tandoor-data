# Open Tandoor Data
This repository contains community contributed data about various data objects that you need for your recipe collection. 

**WIP** This repository currently just contains a work in progress concept of how this database could be structured. 

## Datatypes
This repository contains different datatypes which have the following schema. 

### Food

```json

[
{
  "slug": "<unique_food_slug>",
  "name": "<food_name>",
  "plural_name": "<food_plural_name>",
  "supermarket_category": "<category_slug>",
  "preferred_unit": "<unit_slug>",
  "properties": [
    {
      "property_type": "<property_type_slug>",
      "property_value": "<value_of_property>",
      "food_amount": "<food_amount>",
      "food_unit": "<unit_slug>",
    },
  ]
},


...
]

```



## Contributing
