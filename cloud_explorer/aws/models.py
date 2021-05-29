from django.db import models


class Profile(models.Model):
    region = models.CharField(max_length=50)
    org = models.CharField(max_length=100)
    identifier = models.CharField(max_length=50, unique=True)
    access_key = models.CharField(max_length=250, null=True, blank=True)
    secret_key = models.CharField(max_length=250, null=True, blank=True)
    session_token = models.CharField(max_length=450, null=True, blank=True)

    def __str__(self):
        return f"{self.org}({self.region})"


class HostedZone(models.Model):
    name = models.CharField(max_length=100)
    zone_id = models.CharField(max_length=100)
    account = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'zone_id')

    def __str__(self):
        return self.name
