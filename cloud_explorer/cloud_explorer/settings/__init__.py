import importlib

from .base import *  # noqa

try:
    from .local import *  # noqa
except:  # noqa
    from .production import *  # noqa

# import app feature flags
mod = importlib.import_module('.app_config', __name__)
for setting in dir(mod):
    if setting.isupper():
        setting_value = getattr(mod, setting)
        locals()[f"CE_{setting}"] = f"{setting_value}"
