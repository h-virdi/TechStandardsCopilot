import json


with open(
    "data/taxonomy.json",
    encoding="utf-8"
) as f:

    TAXONOMY = json.load(f)


def get_taxonomy(
    component_description
):

    return TAXONOMY.get(
        component_description,
        {}
    )