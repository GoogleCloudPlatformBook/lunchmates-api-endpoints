#!/usr/bin/env python

from protorpc import remote

from base import lunchmates_api
from base import check_user

from model.model import UserData

@lunchmates_api.api_class(resource_name='user_data', path="users")
class Users(remote.Service):

	@UserData.query_method(query_fields=('limit', 'order', 'pageToken'), name='user.list')
	def list(self, query):
		check_user()
		return query