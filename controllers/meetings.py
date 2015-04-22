#!/usr/bin/env python

from protorpc import remote

from base import lunchmates_api
from base import authenticated_user_data

from model.model import Meeting

@lunchmates_api.api_class(resource_name='meeting')
class Meetings(remote.Service):

    @Meeting.query_method(query_fields=('limit', 'order', 'pageToken'), path='meetings', user_required=True, name='meetings.list')
    def list(self, query):
        return query

    @Meeting.method(path='meetings', name='meetings.create', user_required=True)
    def create(self, meeting):

        meeting.owner = authenticated_user_data().key
        meeting.put()
        return meeting