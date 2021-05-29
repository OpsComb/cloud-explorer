import logging

from kubernetes import client

from k8s.resources import BaseResource, register

logger = logging.getLogger(__name__)


class Namespace(BaseResource):

    api_key = "namespace"
    api_group = "core"  # to be used when multiple api versions available

    def get_namespace_info(self, namespace):
        logger.info("Using context - %s to get namespace info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        logger.debug("Getting info for namespace - %s " % (namespace))
        try:
            response = api_instance.read_namespaced(namespace, pretty='')
            logger.debug("Response for namespace - %s is - %s" % (namespace, response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            if e.status == 404:
                return {}
            else:
                raise Exception(e)

    def get_filtered_namespace_list(self, label_filters, field_filters):
        logger.info("Using context - %s to get list namespace based on filters" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespace(field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return [entry['metadata'] for entry in response.to_dict().get('items', [])]
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(Namespace)
