from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import random
import string
import httplib2

from apiclient.discovery import build


def random_pass() -> str:
    rand = random.SystemRandom()
    pool = string.ascii_letters + string.digits + string.punctuation
    while True:
        passwd = ''.join(rand.choices(pool, k=16))
        # Guarantee digits and punctuation
        if any(x in passwd for x in string.digits) and any(x in passwd for x in string.punctuation):
            return passwd

class User(object):
    def __init__(self, username, secondary_email, first_name=None, last_name=None):
        self.username = username
        self.secondary_email = secondary_email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):
        return "{}@hkn.eecs.berkeley.edu".format(self.username)

    @property
    def json(self):
        return {
            'name': {'familyName': self.last_name, 'givenName': self.first_name},
            'primaryEmail': email,
            'emails': [
                {
                    'address': secondary_email,
                    'type': 'work',
                    'primary': False,
                },
            ],
        }


def add_users(credentials, election_data):
    #create new account for users, by Carolyn Wang, modified by Catherine Hu
    http = credentials.authorize(httplib2.Http())
    service = build('admin', 'directory_v1', http=http)
    if election_data:
        for row in election_data:
            firstName = row[1].strip().capitalize()
            lastName = row[2].strip().capitalize()
            randomPass = random_pass()
            # print(randomPass)
            email = row[3] + '@hkn.eecs.berkeley.edu'
            secondary_email = row[4]
            #TODO: get rid of spaces, capitalize names, error catching
            body = {
                'name': {'familyName': lastName, 'givenName': firstName},
                'password': randomPass,
                'primaryEmail': email,
                'emails': [
                    {
                        'address': secondary_email,
                        'type': 'work',
                        'primary': False,
                    },
                ],
                'changePasswordAtNextLogin': True
            }
            try:
                existing_user = service.users().get(userKey=email).execute()
                print('User already exists: ' + email)
            except Exception as _:
                result = service.users().insert(body=body).execute()
            # print('added ' + email + ' to users')
    return