import logging

from k8s.resources import BaseResource, register
from kubernetes import client

logger = logging.getLogger(__name__)


class ReplicaSet(BaseResource):

    api_key = "replica_set"
    api_group = "apps"  # to be used when multiple api versions available

    def get_replicaset_info(self, replicaset_name, namespace):
        logger.info("Using context - %s to get replicaset info" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        logger.debug("Getting info for replicaset - %s in namespace - %s " % (replicaset_name, namespace))
        try:
            response = api_instance.read_namespaced_replica_set(replicaset_name, namespace, pretty='')
            logger.debug("Response for replicaset - %s from cluster - %s" % (replicaset_name, response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            if e.status == 404:
                return {}
            else:
                raise Exception(e)

    def get_filtered_replicaset_list(self, namespace, label_filters, field_filters):
        logger.info("Using context - %s to get list replicaset based on filters" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.AppsV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_replica_set(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(ReplicaSet)
