import logging

from k8s.resources import BaseResource, register
from kubernetes import client

logger = logging.getLogger(__name__)


class HPA(BaseResource):

    api_key = "horizontal_scaling_params"
    api_group = "autoscaling"  # to be used when multiple api versions available

    def create_horizontal_pod_autoscaler(self, namespace, scaling_json):
        logger.info("Using context - %s to create horizontal pod autoscaler" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AutoscalingV1Api(kube_config)
        try:
            response = api_instance.create_namespaced_horizontal_pod_autoscaler(namespace=namespace, body=scaling_json)
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def update_horizontal_pod_autoscaler(self, hpa_name, changes, namespace):
        logger.info("Using context - %s for updating hpa - %s" % (self.context_name, hpa_name))
        kube_config = self.get_context_config()

        api_instance = client.AutoscalingV1Api(kube_config)
        logger.info("Updating hpa with changes - %s changes - %s" % (hpa_name, changes))
        try:
            response = api_instance.patch_namespaced_horizontal_pod_autoscaler(hpa_name, namespace, changes)
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)

    def get_hpa_info(self, hpa_name, namespace):
        logger.info("Using context - %s to get horizontal pod autoscaler info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AutoscalingV1Api(kube_config)
        logger.debug("Getting info for hpa - %s in namespace - %s " % (hpa_name, namespace))
        try:
            response = api_instance.read_namespaced_horizontal_pod_autoscaler(hpa_name, namespace, pretty='')
            logger.debug("Response for hpa - %s from cluster - %s" % (hpa_name, response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            if e.status == 404:
                return {}
            else:
                raise Exception(e)

    def get_filtered_hpa_list(self, namespace, label_filters, field_filters):
        logger.info("Using context - %s to get list hpa based on filters" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AutoscalingV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_horizontal_pod_autoscaler(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(HPA)
