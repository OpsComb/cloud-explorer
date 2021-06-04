"""
Here you can configure application features and toggle them whenever required

Values must be valid python datatypes. Only UpperCase values are picked.
All values are prefixed with 'CE_' to prevent overriding of core settings.
Eg - if a setting "TEST" is defined here, it will be available as CE_TEST

** in app_config.py **
TEST = True

** in other file **
from django.conf import settings

print(settings.CE_TEST)
>> prints True

"""

TEST = True
