from schema import Optional, And, Use


def _set_function_schema(self):
    _schemas = {
        "create_capacity_provider": {
            "name": And(str, len, Use(str.strip)),
            "autoScalingGroupProvider": {
                "autoScalingGroupArn": And(str, len, Use(str.strip)),
                Optional("managedScaling"): {},
                Optional("managedTerminationProtection"): And(str, len, Use(str.strip))
            },
            "tags": And([
                {
                    'key': And(str, len, Use(str.strip)),
                    'value': And(str, len, Use(str.strip))
                }, Use(self._format_tags)
            ])
        }
    }
    return _schemas
