from django.db import models


# Create your models here.

class WhiteList(models.Model):
    app_name = models.CharField(max_length=256)
    version = models.CharField(max_length=256)
    ip_addr = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.ip_addr}: {self.app_name} {self.version}"

    class Meta:
        unique_together = ("app_name", "version", "ip_addr")


class UnauthorizedApp(models.Model):
    app_name = models.CharField(max_length=256)
    ip_addr = models.CharField(max_length=256)
    reason = models.CharField(max_length=256)  # app reason / version reason
    install_date = models.CharField(max_length=256)  # date-key format YYYYMMDD

    def __str__(self):
        return f"{self.ip_addr}: {self.app_name}"

    class Meta:
        unique_together = ("app_name", "ip_addr")
