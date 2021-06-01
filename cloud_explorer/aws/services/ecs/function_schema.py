from schema import Optional, And, Use, Or

str_check = And(str, len, Use(str.strip))
positive_int_check = And(int, lambda x: x > 0)


def _set_function_schema(self):
    _schemas = {
        "create_capacity_provider": {
            "name": str_check,
            "autoScalingGroupProvider": {
                "autoScalingGroupArn": str_check,
                Optional("managedScaling"): {},
                Optional("managedTerminationProtection"): str_check
            },
            "tags": And([
                {
                    'key': str_check,
                    'value': str_check
                }, Use(self._format_tags)
            ])
        },
        "create_cluster": {
            "clusterName": str_check,
            "tags": And([
                {
                    'key': str_check,
                    'value': str_check
                }, Use(self._format_tags)
            ]),
            Optional("settings"): [
                {
                    "name": str_check,
                    "value": str_check
                }
            ],
            Optional("configuration"): {
                "executeCommandConfiguration": {
                    "kmsKeyId": str_check,
                    "logging": Or("NONE", "DEFAULT", "OVERRIDE"),
                    Optional("logConfiguration"): {
                        "cloudWatchLogGroupName": str_check,
                        "cloudWatchEncryptionEnabled": bool,
                        "s3BucketName": str_check,
                        "s3EncryptionEnabled": bool,
                        "s3KeyPrefix": str_check
                    }
                }
            },
            Optional("capacityProviders"): [str_check],
            Optional("defaultCapacityProviderStrategy"): [
                {
                    "capacityProvider": str_check,
                    "weight": positive_int_check,
                    "base": positive_int_check
                },
            ]
        }
    }
    return _schemas
