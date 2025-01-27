from django.db import models

# Create your models here.


class Voice(models.Model):
    voice = models.FileField(upload_to='user_voice')
