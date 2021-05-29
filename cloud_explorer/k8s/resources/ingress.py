import logging

from k8s.resources import BaseResource, register

logger = logging.getLogger(__name__)


class Ingress(BaseResource):

    api_key = "ingress_params"
    api_group = "extensions"


register(Ingress)
