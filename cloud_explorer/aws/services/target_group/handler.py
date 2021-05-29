import logging
from typing import Dict, List

from cloud_explorer.aws.utils.aws_base import AWSBase
from cloud_explorer.aws.utils.mixins import SchemaMixin

from .function_schema import _set_function_schema

logger = logging.getLogger('__name__')


class TargetGroupHandler(AWSBase, SchemaMixin):
    Profile = "aws-prod"

    def __init__(self, profile=None, *args, **kwargs):
        # create client
        self.profile = profile or TargetGroupHandler.Profile
        self.client = AWSBase().get_client('elbv2', profile=self.profile)
        self.default_pagination = True  # paginate wherever possible
        self.schemas = _set_function_schema(self)
        # TODO: parameterize them per resource
        self.default_tags = []  # format = {""key: "value"}

    def add_tags(self, resource_arns, tags=[]):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})
        tags = self._format_tags(tags)

        if isinstance(resource_arns, str):
            resource_arns = [resource_arns]

        response = self.client.add_tags(
            ResourceArns=resource_arns,
            Tags=tags
        )
        response = self._format_response(response, root_key='')
        return response

    def create_target_group(self, name: str, protocol: str, protocol_version: str, port: int,
                            vpc_id: str, healthcheck_config: Dict, target_type: str, tags: List = []):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})
        tags = self._format_tags(tags)
        response = self.client.create_target_group(
            Name=name,
            Protocol=protocol,
            ProtocolVersion=protocol_version,
            Port=port,
            VpcId=vpc_id,
            TargetType=target_type,
            Tags=tags,
            **healthcheck_config
        )
        response = self._format_response(response, root_key='TargetGroups')
        return response

    def delete_target_group(self, target_group_arn: str):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})
        response = self.client.delete_target_group(
            TargetGroupArn=target_group_arn,
        )
        response = self._format_response(response, root_key='')
        return response

    def deregister_targets(self, target_group_arn: str, targets: List[Dict]):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})
        response = self.client.deregister_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets
        )
        response = self._format_response(response, root_key='')
        return response

    def describe_tags(self, resource_arns: List):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})

        if isinstance(resource_arns, str):
            resource_arns = [resource_arns]

        response = self.client.describe_tags(
            ResourceArns=resource_arns
        )
        response = self._format_response(response, root_key='TagDescriptions')
        return response

    def describe_target_group_attributes(self, tg_arn):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})

        response = self.client.describe_target_group_attributes(
            TargetGroupArn=tg_arn
        )
        response = self._format_response(response, root_key='Attributes')
        return response

    def describe_target_groups(self):
        pass

    def describe_target_health(self, tg_arn: str, targets: List = []):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})

        response = self.client.describe_target_health(
            TargetGroupArn=tg_arn,
            Targets=targets
        )
        response = self._format_response(response, root_key='TargetHealthDescriptions')
        return response

    def modify_target_group(self):
        pass

    def modify_target_group_attributes(self, tg_arn: str, attributes: Dict):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})

        response = self.client.modify_target_group_attributes(
            TargetGroupArn=tg_arn,
            Attributes=attributes
        )
        response = self._format_response(response, root_key='Attributes')
        return response

    def register_targets(self, target_group_arn: str, targets: List[Dict]):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})
        response = self.client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets
        )
        response = self._format_response(response, root_key='')
        return response

    def remove_tags(self, resource_arns: List, tag_keys: List):
        if self.strict_argument_checking:
            # TODO: write schema for this and send arguments accordingly
            self._validate_args({})

        response = self.client.remove_tags(
            ResourceArns=resource_arns,
            TagKeys=tag_keys
        )
        response = self._format_response(response, root_key='')
        return response

    def describe_tg(self, names):
        def f(x):
            return (x.get('TargetGroupName'), x)

        # name can be 1 or a list
        logger.info("Search request for - %s | Profile - %s" % (names, self.profile))

        #  will filter out elements which do not match criteria
        if isinstance(names, (list, tuple)):
            # ensuring elements of list are correct
            names = list(filter(lambda x: isinstance(x, str), names))
            names = list(filter(None, names))
        elif isinstance(names, str):
            names = [names]
        else:
            raise ValueError(
                "Invalid type of argument - names.Expected list or string but got - %s" % (
                    type(names)
                )
            )
        paginator = self.client.get_paginator('describe_target_groups')
        response_iterator = paginator.paginate(Names=names, PaginationConfig={
            "PageSize": 400
        })
        for response in response_iterator:
            yield from map(f, response.get(TargetGroupHandler.ResponseKey))
