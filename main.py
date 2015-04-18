# If you have not yet seen the source in basic/main.py, please take a look.

import config

# Endpoints
import endpoints

# App Engine
import webapp2
from webapp2 import Route
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute

# Controllers
from controllers import meetings
from controllers import meeting_requests
from controllers import users
from controllers import auth

# Task handlers
from tasks.emails import *
from tasks.requests import *

# Endpoints API
app = endpoints.api_server([meetings.Meetings,
                            meeting_requests.MeetingRequests,
                            users.Users,
                            auth.Auth], restricted=False)

# Tasks App Engine API
TASK_ROUTES = [
    DomainRoute(config.subdomain, [ # Allowed domains

        routes.PathPrefixRoute(r'/tasks', [

            # Emails
            Route(r'/email', handler=EmailTaskHandler),

            # Send users a request summary of their pending incoming requests
            Route(r'/request-summary', handler=RequestSummaryHandler)
        ])
    ])
]
tasks = webapp2.WSGIApplication(TASK_ROUTES, debug=True)