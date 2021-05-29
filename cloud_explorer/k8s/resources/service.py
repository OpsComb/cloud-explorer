import logging
from k8s.resources import BaseResource, register

from kubernetes import client

logger = logging.getLogger(__name__)


class Service(BaseResource):

    api_key = "service_params"

    def create_service(self, service_json, namespace=None):
        logger.info("Using context - %s to create service" % (self.context_name))
        kube_config = self.get_context_config()

        namespace = namespace or service_json.get('metadata', {}).pop('namespace', "default")

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Creating service in namespace - %s from json - %s" % (namespace, service_json))
        try:
            response = api_instance.create_namespaced_service(namespace, body=service_json, pretty="true")
            logger.debug("Input JSON - %s | Response from cluster - %s" % (service_json, response))
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def patch_service(self, service_name, changes, namespace=None):
        logger.info("Using context - %s to update service" % (self.context_name))
        kube_config = self.get_context_config()

        namespace = namespace or changes.get('metadata', {}).pop('namespace', "default")

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Updating service in namespace - %s from json - %s" % (namespace, changes))
        try:
            response = api_instance.patch_namespaced_service(service_name, namespace, body=changes, force=False)
            logger.debug("Input JSON - %s | Response from cluster - %s" % (changes, response))
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def get_service_info(self, service_name, namespace):
        logger.info("Using context - %s to get service info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Getting info for service - %s in namespace - %s " % (service_name, namespace))
        try:
            response = api_instance.read_namespaced_service(service_name, namespace, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            if e.status == 404:
                return {}
            else:
                raise Exception(e)

    def get_filtered_service_list(self, namespace, field_filters, label_filters):
        logger.info("Using context - %s to get all services" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Getting all services in namespace - %s " % (namespace))
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_service(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def delete_service(self, service_name, namespace):
        logger.info("Using context - %s for deleting service - %s" % (self.context_name, service_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        try:
            response = api_instance.delete_namespaced_service(service_name, namespace)
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(Service)
