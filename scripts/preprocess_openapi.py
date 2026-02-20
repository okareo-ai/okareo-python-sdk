#!/usr/bin/env python3
"""
Preprocess openapi.json to convert Pydantic v2-style nullable patterns
into a format compatible with openapi-python-client.

Pydantic v2 emits Optional[T] as:
    {"anyOf": [<T_schema>, {"type": "null"}]}

openapi-python-client expects the simpler:
    <T_schema>                       (for path / query parameters)
    <T_schema> + "nullable": true    (for schema properties & request bodies)

This script recursively walks the OpenAPI spec and collapses any
`anyOf` that is simply [<real_type>, {"type": "null"}]` down to
just `<real_type>`, preserving all other `anyOf` unions untouched.

For schema properties (request/response bodies) the collapsed result
keeps ``"nullable": true`` so the generator emits proper None-handling
code. For path and query parameters, nullable is omitted because those
must always carry a value.
"""

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


def is_null_schema(schema: dict) -> bool:
    """Check if a schema is just {"type": "null"} (possibly with extra keys)."""
    return schema.get("type") == "null"


def collapse_nullable_anyof(obj: Any, add_nullable: bool = True) -> Any:
    """
    Recursively walk the OpenAPI spec. When we find an `anyOf` that is
    exactly [<real_schema>, {"type": "null"}] (in either order), replace
    the containing dict with just <real_schema> (merging any sibling keys
    like title, description, default).

    Parameters
    ----------
    add_nullable : bool
        When True the collapsed schema gets ``"nullable": true`` so the
        generator knows the field can be None.  Set to False for path /
        query parameter schemas where null is not a valid value.
    """
    if isinstance(obj, list):
        return [collapse_nullable_anyof(item, add_nullable) for item in obj]

    if not isinstance(obj, dict):
        return obj

    # Detect path / query parameters — their "schema" child must NOT
    # be marked nullable (the value is always present in the URL).
    is_param = obj.get("in") in ("path", "query")

    # Recurse into all values, suppressing nullable for param schemas
    new_obj = {}
    for k, v in obj.items():
        if k == "schema" and is_param:
            new_obj[k] = collapse_nullable_anyof(v, add_nullable=False)
        else:
            new_obj[k] = collapse_nullable_anyof(v, add_nullable)
    obj = new_obj

    if "anyOf" in obj and isinstance(obj["anyOf"], list):
        schemas = obj["anyOf"]
        null_schemas = [s for s in schemas if is_null_schema(s)]
        non_null_schemas = [s for s in schemas if not is_null_schema(s)]

        # Only collapse when it's exactly one real type + one null type
        if len(null_schemas) == 1 and len(non_null_schemas) == 1:
            real_schema = deepcopy(non_null_schemas[0])

            # Carry over sibling keys (title, description, default, etc.)
            sibling_keys = {k: v for k, v in obj.items() if k != "anyOf"}
            for key, value in sibling_keys.items():
                if key not in real_schema:
                    real_schema[key] = value

            # Preserve nullability for non-parameter schemas
            if add_nullable:
                real_schema["nullable"] = True

            return real_schema

    return obj


def mark_optional_properties_nullable(spec: dict) -> dict:
    """
    In OpenAPI 3.0.x, ``nullable: true`` is the way to indicate a field can
    be ``null``.  FastAPI + Pydantic v2 often omits this marker for
    ``Optional[T]`` fields when generating a 3.0.x spec.

    This function walks every component schema and adds ``nullable: true``
    to every property that is **not** listed in ``required``.  This is safe
    because:
    -  If the API never actually returns ``null`` for a field the generated
       None-branch is simply unused.
    -  If the API *does* return ``null`` (common for optional fields) the
       generated ``from_dict`` will handle it instead of crashing.
    """
    schemas = spec.get("components", {}).get("schemas", {})
    for schema in schemas.values():
        properties = schema.get("properties")
        if not properties:
            continue
        required = set(schema.get("required", []))
        for prop_name, prop_schema in properties.items():
            if prop_name not in required and "nullable" not in prop_schema:
                # Don't mark nullable if the property has a non-None default
                # (e.g. default: {}) — the generator rejects nullable fields
                # whose default is not None.
                default = prop_schema.get("default")
                if "default" in prop_schema and default is not None:
                    continue
                prop_schema["nullable"] = True
    return spec


def main() -> None:
    if len(sys.argv) < 2:
        input_path = Path("openapi.json")
    else:
        input_path = Path(sys.argv[1])

    if len(sys.argv) < 3:
        output_path = input_path  # overwrite in place
    else:
        output_path = Path(sys.argv[2])

    with open(input_path) as f:
        spec = json.load(f)

    spec = collapse_nullable_anyof(spec)
    spec = mark_optional_properties_nullable(spec)

    with open(output_path, "w") as f:
        json.dump(spec, f, indent=2)

    print(f"Preprocessed {input_path} -> {output_path}")


if __name__ == "__main__":
    main()
