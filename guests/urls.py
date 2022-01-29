from django.urls import re_path

from guests.views import GuestListView, guest_importer, test_email, export_guests, \
    invitation, rsvp_confirm, dashboard, rsvp

urlpatterns = [
    re_path(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    re_path(r'^dashboard/$', dashboard, name='dashboard'),
    re_path(r'^guests/export$', export_guests, name='export-guest-list'),
    re_path(r'^invite/', invitation, name='invitation'),
    re_path(r'^email-test/(?P<template_id>[\w-]+)/$', test_email, name='test-email'),
    re_path(r'^rsvp/confirm/(?P<invite_id>[\w-]+)/$', rsvp_confirm, name='rsvp-confirm'),
    re_path(r'^rsvp/', rsvp, name='rsvp'),
    re_path(r'^importer', guest_importer, name='guest_importer')
]
