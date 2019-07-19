from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Den_profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
  follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

User.den_profile = property(lambda u: Den_profile.objects.get_or_create(user=u)[0])
