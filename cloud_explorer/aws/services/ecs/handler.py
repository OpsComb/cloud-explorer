""" This file contains utility functions for ECS operations """
import logging
from typing import List

from cloud_explorer.aws.utils.aws_base import AWSBase
from cloud_explorer.aws.utils.mixins import SchemaMixin
from .function_schema import _set_function_schema

logger = logging.getLogger('__name__')


class ECSHandler(AWSBase, SchemaMixin):
    Profile = "aws-prod"

    def __init__(self, profile=None, *args, **kwargs):
        # create client
        self.profile = profile or ECSHandler.Profile
        self.client = AWSBase()._get_client('ecs', profile=profile)
        self.default_pagination = True  # paginate wherever possible
        self.schemas = _set_function_schema(self)
        # TODO: parameterize them per resource
        self.default_tags = []  # format = {""key: "value"}

    def create_capacity_provider(self, **kwargs):
        self._validate_args(kwargs)
        response = self.client.create_capacity_provider(**kwargs)
        response = self._format_response(response, root_key='capacityProvider')
        return response

    def create_cluster(self, **kwargs):
        # TODO: write schema for this and send arguments accordingly
        self._validate_args(kwargs)
        response = self.client.create_cluster(**kwargs)
        response = self._format_response(response, root_key='cluster')
        return response

    def create_service(self, **kwargs):
        # TODO: write schema for this and send arguments accordingly
        self._validate_args(kwargs)
        response = self.client.create_service(**kwargs)
        response = self._format_response(response, root_key='service')
        return response

    def create_task_set(self):
        pass

    def delete_account_setting(self):
        pass

    def delete_capacity_provider(self):
        pass

    def delete_cluster(self):
        pass

    def delete_service(self):
        pass

    def delete_task_set(self):
        pass

    def deregister_container_instance(self):
        pass

    def deregister_task_definition(self):
        pass

    def describe_capacity_providers(self):
        pass

    def describe_clusters(self, cluster_list: List[str], include: List[str] = []):
        valid_inclusions = set(["ATTACHMENTS", "CONFIGURATIONS", "SETTINGS", "STATISTICS", "TAGS"])
        # if cluster list is empty, details of 'default' cluster is returned
        assert cluster_list, "Empty cluster_list received"

        inclusions = list(valid_inclusions.intersection(set(include)))
        aws_response = self.client.describe_clusters(
            clusters=cluster_list,
            include=inclusions
        )
        return aws_response

    def describe_container_instances(self):
        pass

    def describe_services(self):
        pass

    def describe_task_definition(self):
        pass

    def describe_task_sets(self):
        pass

    def describe_tasks(self):
        pass

    def execute_command(self):
        pass

    def list_clusters(self):
        pass

    def list_container_instances(self):
        pass

    def list_services(self):
        pass

    def list_tags_for_resource(self):
        pass

    def list_task_definition_families(self):
        pass

    def list_task_definitions(self):
        pass

    def list_tasks(self):
        pass

    def put_cluster_capacity_providers(self):
        pass

    def register_container_instance(self):
        pass

    def register_task_definition(self):
        pass

    def run_task(self):
        pass

    def start_task(self):
        pass

    def stop_task(self):
        pass

    def submit_attachment_state_changes(self):
        pass

    def submit_container_state_change(self):
        pass

    def submit_task_state_change(self):
        pass

    def tag_resource(self):
        pass

    def untag_resource(self):
        pass

    def update_capacity_provider(self):
        pass

    def update_cluster(self):
        pass

    def update_cluster_settings(self):
        pass

    def update_container_agent(self):
        pass

    def update_container_instances_state(self):
        pass

    def update_service(self):
        pass

    def update_service_primary_task_set(self):
        pass

    def update_task_set(self):
        pass
