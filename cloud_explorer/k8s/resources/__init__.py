import logging

from kubernetes import client

logger = logging.getLogger(__name__)


class BaseResource(object):

    def __init__(self, context_name):
        self.context_name = context_name

    @classmethod
    def name(cls):
        return cls.__name__

    @classmethod
    def type(cls):
        return cls.__name__.lower()

    @classmethod
    def configuration_schema(cls):
        return {}

    @classmethod
    def api_versions_supported(cls):
        return ["v1"]

    def get_context_config(self):
        host, token = self._get_cluster_details(self.context_name)
        configuration = client.Configuration()
        configuration.host = host
        configuration.api_key['authorization'] = token
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.verify_ssl = False
        return client.ApiClient(configuration)

    def _get_cluster_details(self, cluster):
        pass


resource_dict = {}


def get_resource_class(resource_name, api_version):
    # get class
    if resource_name.lower() not in resource_dict:
        raise KeyError("Resource - %s is not registered" % (resource_name))
    resource_class = resource_dict[resource_name]
    if api_version in resource_class.api_versions_supported():
        return resource_class
    else:
        raise Exception("The API Version - %s is not supported by resource - %s" % (api_version, resource_name))


def register(resource_class):
    global resource_dict
    assert issubclass(resource_class, BaseResource), "Resource class - %s must be of BaseResource Type" % (resource_class.__name__)
    logger.info("Registering resource - %s" % (resource_class.type()))
    resource_dict[resource_class.type()] = resource_class


def load_all_resources():
    import glob
    from os.path import basename, dirname, isfile, join
    modules = glob.glob(join(dirname(__file__), "*.py"))
    # remove last 3 characters to remove *.py extension
    modules_to_be_imported = ["k8s.resources.%s" % (basename(f[:-3])) for f in modules if isfile(f) and not f.endswith('__init__.py')]
    map(__import__, modules_to_be_imported)


load_all_resources()
