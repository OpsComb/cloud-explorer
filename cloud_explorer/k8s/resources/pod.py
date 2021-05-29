import logging

from k8s.resources import BaseResource, register
from kubernetes import client

logger = logging.getLogger(__name__)


class Pod(BaseResource):

    api_key = "pod_params"

    def get_filtered_pod_list(self, namespace, label_filters, field_filters):
        logger.info("Using context - %s to filter pod list" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_pod(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def get_pod_info(self, namespace, name):
        logger.info("Using context - %s to get pod info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        try:
            response = api_instance.read_namespaced_pod(name, namespace, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def put_pod(self, pod_json, namespace=None):
        logger.info("Using context - %s to create pod" % (self.context_name))
        kube_config = self.get_context_config(self.context_name)

        namespace = namespace or pod_json.get('metadata', {}).pop('namespace', "default")

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Creating pod in namespace - %s from json - %s" % (namespace, pod_json))
        try:
            response = api_instance.create_namespaced_pod(namespace, body=pod_json, pretty="true")
            logger.debug("Input JSON - %s | Response from cluster - %s" % (pod_json, response))
        except client.rest.ApiException as e:
            logger.exception(e)


register(Pod)
