import csv
import io
import uuid
from guests.models import Party, Guest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def import_guests(path):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            party_name, first_name, last_name, party_type = row[:3]
            if not party_name:
                print ('skipping row {}'.format(row))
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            party.type = party_type
            party.save()
            guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            guest.save()


def export_guests():
    headers = [
        'party_name', 'first_name', 'last_name', 'party_type',
        'category', 'is_attending', 'rehearsal_dinner', 'meal', 'comments'
    ]
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    party.type,
                    guest.is_attending,
                    party.rehearsal_dinner,
                    guest.meal,
                    party.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes', 't', 'true', '1')
