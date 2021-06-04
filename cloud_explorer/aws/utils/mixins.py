from typing import Dict

from schema import Schema


class SchemaNotFoundError(Exception):
    pass


class SchemaMixin:

    def _set_function_schema(self):
        return None

    def _get_function_schema(self, function_name: str):
        if function_name in self.schemas:
            yield self.schemas[function_name]
        else:
            raise SchemaNotFoundError(f"The finction - {function_name} has no registered schema")

    def _validate_schema(self, function_name: str, kwargs: Dict):
        schema = self._get_function_schema(function_name)
        schema_obj = Schema(schema, ignore_extra_keys=True)
        return schema_obj.validate(kwargs)
