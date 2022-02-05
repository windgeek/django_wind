# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import django


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, primary_key=True, db_index=True)
    password = models.CharField(max_length=100, null=False)

