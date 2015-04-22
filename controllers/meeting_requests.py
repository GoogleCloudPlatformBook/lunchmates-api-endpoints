#!/usr/bin/env python

import endpoints
from protorpc import remote

from base import lunchmates_api
from base import authenticated_user_data

from model.model import MeetingRequest
from google.appengine.api import taskqueue

@lunchmates_api.api_class(resource_name='meeting_request', path="meetings")
class MeetingRequests(remote.Service):

    @MeetingRequest.query_method(query_fields=('meeting_id',), path='{meeting_id}/requests', user_required=True, name='meeting_requests.list')
    def list(self, query):
        return query.order(-MeetingRequest.created)

    @MeetingRequest.method(path='{meeting_id}/join', user_required=True, name='meeting_requests.create')
    def create(self, meeting_request):

        meeting_request.parent = authenticated_user_data().key

        # Schedule task to send email
        meeting = meeting_request.meeting.get()
        params = {'owner_id': meeting.owner.id(), 'nickname':endpoints.get_current_user().nickname()}
        taskqueue.add(queue_name='email', url='/tasks/email', params=params)

        meeting_request.put()
        return meeting_request
