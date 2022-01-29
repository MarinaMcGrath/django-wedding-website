import base64
from collections import namedtuple
from http.client import HTTPResponse
import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from guests import csv_import
from guests.invitation import INVITATION_TEMPLATE, guess_party_by_invite_id_or_404
from guests.models import Guest, MEALS, Party
from guests.save_the_date import get_save_the_date_context, send_save_the_date_email, SAVE_THE_DATE_TEMPLATE, \
    SAVE_THE_DATE_CONTEXT_MAP


class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    parties_with_pending_invites = Party.objects.filter(is_attending=None).order_by('category', 'name')
    attending_guests = Guest.objects.filter(is_attending=True)
    guests_without_meals = attending_guests.filter(
        Q(meal__isnull=True) | Q(meal='')
    ).order_by('first_name')
    meal_breakdown = attending_guests.exclude(meal=None).values('meal').annotate(count=Count('*'))
    return render(request, 'guests/dashboard.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'guests': Guest.objects.filter(is_attending=True).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'guests_without_meals': guests_without_meals,
        'meal_breakdown': meal_breakdown,
    })


def rsvp(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'guests/rsvp.html', context)
    elif request.method == 'POST':
        template_name='guests/rsvp.html'
        submited_full_name = request.POST['party'].lower()
        if ' ' not in submited_full_name:
            context['error'] = True

        try:
            first_name = submited_full_name.split(' ')[0]
            last_name = submited_full_name.split(' ')[1]
        except Exception:
            context['error'] = True

        if 'error' not in context:
            guest = list(Guest.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name))
            if len(guest) > 0:
                context['party'] = guest[0].party
                context['meals'] = MEALS
                template_name='guests/invitation.html'
            else:
                context['error'] = True
        return render(request, template_name=template_name, context=context)
    return HTTPResponse(405)


def invitation(request):
    if request.method == 'POST':
        for response in _parse_invite_params(request.POST):
            guest = Guest.objects.get(pk=response.guest_pk)
            party = guest.party
            guest.is_attending = response.is_attending
            guest.meal = response.meal
            guest.save()
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            party.comments = comments if not party.comments else '{}; {}'.format(party.comments, comments)
        party.is_attending = party.any_guests_attending
        party.save()
        context = {
            'party': party
        }
        return render(request, template_name='guests/rsvp_confirm.html', context=context)
    return HttpResponse(404)


InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'is_attending', 'meal'])


def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith('attending'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['attending'] = True if value == 'yes' else False
            responses[pk] = response
        elif param.startswith('meal'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['meal'] = value
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(pk, response['attending'], response.get('meal', None))


def rsvp_confirm(request, invite_id=None):
    party = guess_party_by_invite_id_or_404(invite_id)
    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'party': party,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })


@login_required
def test_email(request, template_id):
    context = get_save_the_date_context(template_id)
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse('sent!')


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())


@login_required
def guest_importer(request):
    context = {}
    guests = list(Guest.objects.all())
    parties = list(Party.objects.all())
    if request.method == 'GET':
        context['guests'] = guests
        context['parties'] = parties
        return render(request, 'guests/importer.html', context=context)
    if request.method == 'POST':
        fguests = []
        fparties = []
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                print('File is not CSV type')
                return HttpResponse('SUCKS')
            if csv_file.multiple_chunks():
                print(r"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponse('SUCKS')
            file_data = csv_file.read().decode("utf-8")		

            lines = file_data.split("\n")
            for line in lines:
                l = line.split(',')
                party_name, first_name, last_name, party_type = l[:4]
                party_t = party_type.split('\r')[0]
                fguests.append(f'{first_name} {last_name}')
                fparties.append(f'{party_name} {party_t}')
                party = Party.objects.get_or_create(name=party_name)[0]
                party.type = party_t
                party.save()
                guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
                guest.save()
        except Exception as e:
            context['error'] = f'top: {str(e)}'
        try:
            context['guests'] = fguests
            context['parties'] = fparties
        except Exception as e:
            context['error'] = f'bottom: {str(e)}'
        return render(request, 'guests/importer.html', context=context)    
    

