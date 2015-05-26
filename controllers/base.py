#!/usr/bin/env python

import endpoints

from model.model import UserData

# Client IDs
G_DOMAIN = '.apps.googleusercontent.com'
WEBAPP_CLIENT_ID = '99886669718-6q66jlok7oej4bbgfn1nhu5g5gdgak4n' + G_DOMAIN
IOS_CLIENT_ID = '99886669718-gf6eup115gtto53puflik7gpqgcfk9cr' + G_DOMAIN
ANDROID_CLIENT_ID = '99886669718-u0hob6t430emce4mtsajc9lma04hhdu1' + G_DOMAIN
ANDROID_AUDIENCE = WEBAPP_CLIENT_ID

lunchmates_api = endpoints.api(name='lunchmates', version='v1',
                               description='LunchMates API',
                               allowed_client_ids=[
                                    WEBAPP_CLIENT_ID,
                                    IOS_CLIENT_ID,
                                    ANDROID_CLIENT_ID,
                                    endpoints.API_EXPLORER_CLIENT_ID],
                               audiences=[ANDROID_AUDIENCE])


def authenticated_user_data():

    current_user_data = UserData.query(
        UserData.auth_user == endpoints.get_current_user()).get()

    if current_user_data is None:
        raise endpoints.UnauthorizedException()

    return current_user_data
