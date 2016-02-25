from __future__ import unicode_literals
from django.contrib.auth.models import User as AuthUser # pylint: disable=unused-import

from django.db import models # pylint: disable=unused-import



class User(AuthUser): # pylint: disable=no-init
    quota = models.IntegerField(default=1024)

    def hquota(self, unit):
        if unit == 'MB':
            return self.quota/1048576.0
        elif unit == 'GB':
            return self.quota/1073741824.0
        else:
            return 'Unknown unit'
    @property
    def used_quota(self):
        used = User.objects.filter(username=self.username).aggregate(models.Sum('document__file_size'))['document__file_size__sum']
        if used:
            return used
        else:
            return 0

    @property
    def balance_quota(self):
        return self.quota - self.used_quota




class Document(models.Model):
    file_name = models.CharField(max_length=30)
    file_type = models.CharField(max_length=10)
    file_size = models.IntegerField()
    upload_time = models.DateTimeField(auto_now=True)
    hash_address = models.CharField(max_length=40)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    
