#!/usr/bin/env python

import endpoints
from protorpc import remote

from base import lunchmates_api
from base import authenticated_user_data

from google.appengine.ext import ndb

from model.model import UserData
from model import model

USER_EXISTS = 'user_already_exists'

@lunchmates_api.api_class(resource_name='auth')
class Auth(remote.Service):

	@UserData.method(request_fields=(), path='authenticate', http_method='POST', user_required=True, name='user.authenticate')
	def authenticate(self, user):

		user_data = authenticated_user_data()
		if user_data is None:
			return UserData.create_user(endpoints.get_current_user(), model.PROVIDER_GOOGLE)

		else:
			raise endpoints.ForbiddenException(USER_EXISTS)