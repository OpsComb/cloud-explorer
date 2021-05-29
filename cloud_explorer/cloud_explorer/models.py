from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_rate_limit(value):
    splitted_value = value.split("/")
    if not len(splitted_value) == 2:
        raise ValidationError(_("Expected rate limit in form <limit>/<period> eg. 5/min"))

    num, period = splitted_value
    num = int(num)
    duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    if period[0] not in duration:
        raise ValidationError(
            _(f'{period} is not a valid value for period')
        )


class UserRateLimit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate_limit = models.CharField(max_length=100, validators=[validate_rate_limit])

    def __str__(self):
        return f"{self.user} - {self.rate_limit}"
