from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver

ALLOWED_TYPES = [
    ('marina_family', 'marina_family'),
    ('eric_family', 'eric_family'),
    ('marina_friend', 'marina_friend'),
    ('eric_friend', 'eric_friend'),
]


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    display_name = models.CharField(max_length=40, null=True, blank=True)
    type = models.CharField(max_length=13, choices=ALLOWED_TYPES)
    category = models.CharField(max_length=20, null=True, blank=True)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.BooleanField(default=None, null=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))


MEALS = [
    ('vegetarian', 'vegetarian'),
    ('vegan', 'vegan'),
    ('none', 'none')
]


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    is_attending = models.BooleanField(default=None, null=True)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
