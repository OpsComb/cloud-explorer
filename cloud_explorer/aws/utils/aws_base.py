import inspect
import logging
from typing import Dict

import boto3

from cloud_explorer.aws.models import Profile

from .decorators import error_handling_decorator

logger = logging.getLogger(__name__)


# This is a metaclass which will wrap all functions and apply transformation directly to all handlers
class Meta(type):
    def __new__(mcs, name, bases, attrs, *args, **kwargs):
        logger.info('  Meta.__new__(mcs=%s, name=%r, bases=%s, attrs=[%s], args=%s, kwargs=%s)' % (mcs, name, bases, ', '.join(attrs), args, kwargs))
        for attr in attrs:
            value = attrs[attr]
            if callable(value) and not attr.startswith("_"):
                attrs[attr] = error_handling_decorator(value)
        return type.__new__(mcs, name, bases, attrs)


class AWSBase(metaclass=Meta):
    profile = "aws-prod"

    def _get_client(self, service: str, profile: str, **kwargs):
        client_profile = profile or AWSBase.profile
        logger.info(f"Creating client for service - {service} | Profile - {client_profile}")
        profile_details = Profile.objects.get(identifier=client_profile)

        client = boto3.Session(
            aws_access_key_id=profile_details.access_key,
            aws_secret_access_key=profile_details.secret_key,
            region_name=profile_details.region
        ).client(service, **kwargs)

        return client

    def _get_resource(self, service: str, profile: str, **kwargs):
        resource_profile = profile or AWSBase.profile
        logger.info(f"Creating resource for service - {service} | Profile - {resource_profile}")
        profile_details = Profile.objects.get(identifier=resource_profile)

        resource = boto3.Session(
            aws_access_key_id=profile_details.access_key,
            aws_secret_access_key=profile_details.secret_key,
            region_name=profile_details.region
        ).resource(service, **kwargs)

        return resource

    """
    Keeping this function here, since schemaMixin can be removed but removing this from
    every function is difficult.
    """

    def _validate_args(self, kwarg_dict) -> Dict:
        """
            Validates kwargs against schema supplied. Raise exception if schema doesn't match
        """
        caller_function = inspect.stack()[1].function

        if not hasattr(self, "_validate_schema"):
            logger.info(f"Validation disabled for function - {caller_function} | Args Received - {kwarg_dict}")
            return kwarg_dict

        # raise any exceptions directly
        return self._validate_schema(caller_function, kwarg_dict)

    def _format_tags(self, tags):
        """
            Applies any common modifications required on tags
        """
        if not self.default_tags:
            return tags
        else:
            # format tags and check if keys for default tags are present
            formatted_tags = {tag['key']: tag['value'] for tag in tags}
            for key, value in self.default_tags:
                if key in formatted_tags:
                    continue
                else:
                    tags.append({"key": key, "value": value})
        return tags

    def _format_response(self, response, root_key, response_type="dict", output_response_type="dict"):
        # TODO: complete this function
        return response
