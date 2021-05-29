import logging

from kubernetes import client

from k8s.resources import BaseResource, register

logger = logging.getLogger(__name__)


class Deployment(BaseResource):

    api_key = "deployment_params"
    api_group = "apps"  # to be used when multiple api versions available

    def create_deployment(self, deployment_json, namespace=None):
        logger.info("Using context - %s to create deployment" % (self.context_name))
        kube_config = self.get_context_config()

        namespace = namespace or deployment_json.get('metadata', {}).pop('namespace', "default")

        api_instance = client.AppsV1Api(kube_config)
        logger.debug("Creating deployment in namespace - %s from json - %s" % (namespace, deployment_json))
        try:
            response = api_instance.create_namespaced_deployment(
                namespace, body=deployment_json, pretty="true"
            )
            logger.debug("Input JSON - %s | Response from cluster - %s" % (deployment_json, response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def patch_deployment(self, deployment_name, changes, namespace, force=True):
        logger.info("Using context - %s for updating deployment - %s" % (self.context_name, deployment_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        logger.info("Updating deployment with changes - %s changes - %s" % (deployment_name, changes))
        try:
            response = api_instance.patch_namespaced_deployment(deployment_name, namespace, changes, force=True)
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def get_deployment_status(self, deployment_name, namespace):
        logger.info("Using context - %s for updating deployment" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        logger.info("Getting status for deployment - %s in namespace - %s" % (deployment_name, namespace))
        try:
            response = api_instance.read_namespaced_deployment_status(
                deployment_name, namespace
            )
            logger.debug("Status for deployment - %s in namespace - %s is - %s" % (
                deployment_name, namespace, response
            )
            )
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def get_deployment_info(self, deployment_name, namespace):
        logger.info("Using context - %s to get deployment info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        logger.debug("Getting info for deployment - %s in namespace - %s " % (deployment_name, namespace))
        try:
            response = api_instance.read_namespaced_deployment(deployment_name, namespace, pretty='')
            logger.debug("Response for deployment - %s from cluster - %s" % (deployment_name, response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            if e.status == 404:
                return {}
            else:
                raise Exception(e)

    def get_filtered_deployment_list(self, namespace, label_filters, field_filters):
        logger.info("Using context - %s to get list deployments based on filters" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_deployment(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def rollback_deployment(self, deployment_name, namespace):
        logger.info("Using context - %s to get all deployments" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.ExtensionsV1beta1Api(kube_config)
        logger.debug("Rolling back deployment in namespace - %s " % (namespace))

        try:
            # rollback version is optional. not to be added
            rollback_config = {
                "name": deployment_name,
                "rollback_to": 0
            }
            response = api_instance.create_namespaced_deployment_rollback(name=deployment_name, namespace=namespace, body=rollback_config, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def delete_deployment(self, deployment_name, namespace):
        logger.info("Using context - %s for deleting deployment - %s" % (self.context_name, deployment_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        try:
            response = api_instance.delete_namespaced_deployment(deployment_name, namespace)
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(Deployment)
