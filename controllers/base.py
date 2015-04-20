#!/usr/bin/env python

import endpoints

from model.model import UserData

# Client IDs
WEBAPP_CLIENT_ID = '1034740665071-bb97182bfolv75ta7rahan0o0i9aoo09.apps.googleusercontent.com'
IOS_CLIENT_ID = '1034740665071-3m8fbvau4uba692q82ktpo7qqv28cr9n.apps.googleusercontent.com'
ANDROID_CLIENT_ID = '1034740665071-3avud6mj5aebprs04scmqkufqjdugn5u.apps.googleusercontent.com'
ANDROID_AUDIENCE = WEBAPP_CLIENT_ID

lunchmates_api = endpoints.api(name='lunchmates', version='v1', 
							   description='LunchMates API',
							   allowed_client_ids=[WEBAPP_CLIENT_ID,
							   					   IOS_CLIENT_ID,
							   					   ANDROID_CLIENT_ID,
							   					   endpoints.API_EXPLORER_CLIENT_ID],
							   audiences=[ANDROID_AUDIENCE])


def authenticated_user_data():

	current_user_data = UserData.query(UserData.auth_user == endpoints.get_current_user()).get()
	if current_user_data is None:
		raise endpoints.UnauthorizedException(NOT_AUTHORIZED)

	return current_user_data