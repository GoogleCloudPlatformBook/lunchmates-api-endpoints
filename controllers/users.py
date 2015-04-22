#!/usr/bin/env python

from protorpc import remote

from base import lunchmates_api

from model.model import UserData

@lunchmates_api.api_class(resource_name='user_data')
class Users(remote.Service):

	@UserData.query_method(query_fields=('limit', 'order', 'pageToken'), path='users', user_required=True, name='users.list')
	def list(self, query):
		return query