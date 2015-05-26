#!/usr/bin/env python

import endpoints
from protorpc import remote

from base import lunchmates_api
from base import authenticated_user_data

from model.model import UserData
from model import model

USER_EXISTS = 'user_already_exists'


@lunchmates_api.api_class(resource_name='auth')
class Auth(remote.Service):

    @UserData.method(request_fields=(), path='authenticate',
                     user_required=True, name='users.authenticate')
    def authenticate(self, user):

        try:
            authenticated_user_data()
            raise endpoints.ForbiddenException(USER_EXISTS)

        except endpoints.UnauthorizedException:
            return UserData.create_user(endpoints.get_current_user(),
                                        model.PROVIDER_GOOGLE)
