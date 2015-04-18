#!/usr/bin/env python

from protorpc import remote

from base import lunchmates_api
from base import check_user
from base import authenticated_user_data

from model.model import Meeting

@lunchmates_api.api_class(resource_name='meeting', path="meetings")
class Meetings(remote.Service):

    @Meeting.query_method(query_fields=('limit', 'order', 'pageToken'), name='meeting.list')
    def list(self, query):
        check_user()
        return query

    @Meeting.method(http_method='POST', name='meeting.create')
    def create(self, meeting):
        check_user()

        meeting.owner = authenticated_user_data().key
        meeting.put()
        return meeting