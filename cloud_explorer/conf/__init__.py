import importlib

from django.conf import LazySettings

_SETTINGS_PREFIX = "CE"

# import app feature flags
settings_dict = {}

mod = importlib.import_module('.app_settings.py', __name__)
for setting in dir(mod):
    if setting.isupper():
        setting_value = getattr(mod, setting)
        settings_dict[f"{_SETTINGS_PREFIX}_{setting}"] = f"{setting_value}"

app_settings = LazySettings()
app_settings.configure(default_settings=settings_dict)
