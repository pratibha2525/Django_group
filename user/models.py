from django.db import models
from django_mysql.models.fields import JSONField
from django.db.models import IntegerField, Model

class Choice(models.Model):
    choice_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_name

class Group(models.Model):
    group_name = models.CharField(max_length=100)
    choices_list = JSONField()
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'db_group'

    def __str__(self):
        return self.group_name






