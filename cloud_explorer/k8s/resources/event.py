import logging

from k8s.resources import BaseResource, register
from kubernetes import client

logger = logging.getLogger(__name__)


class Event(BaseResource):

    api_key = "events"
    api_group = "core"  # to be used when multiple api versions available

    def get_event_info(self, namespace, name):
        return True

    def get_filtered_events(self, namespace, label_filters, field_filters):
        logger.info("Using context - %s to filter namespace events" % (self.context_name))
        kube_config = self.get_context_config()

        api_instance = client.CoreV1Api(kube_config)
        try:
            field_selector = ",".join(map("=".join, field_filters))
            label_selector = ",".join(map("=".join, label_filters))

            response = api_instance.list_namespaced_event(namespace, field_selector=field_selector, label_selector=label_selector, limit=100, pretty='')
            logger.debug("Response from cluster - %s" % (response))
            return response.to_dict()
        except client.rest.ApiException as e:
            logger.exception(e)
            raise Exception(e)


register(Event)
