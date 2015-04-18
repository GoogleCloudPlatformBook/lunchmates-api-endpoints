#!/usr/bin/env python

import unicodedata

from protorpc import messages

from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsDateTimeProperty
from endpoints_proto_datastore.ndb import EndpointsComputedProperty

from google.appengine.ext import ndb
from google.appengine.ext.ndb import UserProperty

PROVIDER_GOOGLE = 'google'
PROVIDER_FACEBOOK = 'facebook'

DATE_FORMAT_STR = '%Y-%m-%dT%H:%MZ'

class BaseModel(EndpointsModel):
    created = ndb.DateTimeProperty(auto_now_add=True)

    @EndpointsAliasProperty(property_type=messages.IntegerField)
    def id(self):
        return self.key.id()

    def __hash__(self):
        return self.key.id()

    def __eq__(self, other):
        return self.key.id() == other.key.id()
      

class UserData(BaseModel):

    _message_fields_schema = ('created','id','auth_provider','name','email')

    auth_provider = ndb.StringProperty(choices=[PROVIDER_GOOGLE, PROVIDER_FACEBOOK], required=True)
    name = ndb.StringProperty(default='')
    search_name = EndpointsComputedProperty(lambda self: unicodedata.normalize('NFKD', unicode(self.name)).encode('ascii','ignore').lower())
    email = ndb.StringProperty(required=True)
    auth_user = ndb.UserProperty()

    @classmethod
    def create_user(cls, external_user, provider):

        user = UserData(auth_provider=provider)
        
        if provider == PROVIDER_GOOGLE:
            user.auth_user = external_user
            user.email = external_user.email()
            user.name = external_user.nickname()

        elif provider == PROVIDER_FACEBOOK:
            pass

        else:
            raise ValueError('Provider is unknown: ' + provider)

        user.put()
        return user


class Meeting(BaseModel):

    _message_fields_schema = ('created','id','owner_id','venue_forsquare_id','location','earliest_possible_start','latest_possible_start','topic','type','tags')

    owner = ndb.KeyProperty(kind=UserData)
    venue_forsquare_id = ndb.StringProperty(required=True)
    location = ndb.GeoPtProperty()
    earliest_possible_start = EndpointsDateTimeProperty(required=True, string_format=DATE_FORMAT_STR)
    latest_possible_start = EndpointsDateTimeProperty(string_format=DATE_FORMAT_STR)
    topic = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=['drink', 'lunch', 'brunch'])
    tags = ndb.StringProperty(repeated=True)

    @EndpointsAliasProperty(property_type=messages.IntegerField)
    def owner_id(self):
        return self.owner.id()


class MeetingCounter(ndb.Model):
    count = ndb.IntegerProperty(default=0)

    @classmethod
    @ndb.transactional
    def increment(cls, user_key):
        counter = cls.get_by_id(user_key.id())
        if counter is None:
            counter = cls(id=user_key.id())

        counter.count += 1
        counter.put()


class MeetingRequest(BaseModel):

    _message_fields_schema = ('created','id','meeting_id','state')

    meeting = ndb.KeyProperty(kind=Meeting, required=True)
    state = ndb.StringProperty(default='pending', choices=['pending', 'accepted', 'rejected'])

    def ParentMeetingSet(self, value):
        meeting_key = ndb.Key(Meeting, int(value))
        self.meeting = meeting_key
        self._endpoints_query_info.meeting = meeting_key

    @EndpointsAliasProperty(required=True, setter=ParentMeetingSet, property_type=messages.IntegerField)
    def meeting_id(self):
        return self.meeting.id()


