""" Back end for Tyndr implemented using Google Cloud Endpoints.

M: models.py
V: tyndr_api.py
C: messages.py
"""

import endpoints
# Message passing
from protorpc import messages
from protorpc import message_types
from protorpc import remote

# Database access
from google.appengine.api import users
from google.appengine.ext import ndb

# Models
from models import *
# Messages
from messages import *

WEB_CLIENT_ID = ''
ANDROID_CLIENT_ID = ''
IOS_CLIENT_ID = ''
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'tyndr-server'

# Default advert categories
FOUND_PETS = 'found_pets'
LOST_PETS = 'lost_pets'


@endpoints.api(name='tyndr', version='v1',
	       allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
		       		   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
	       audiences=[ANDROID_AUDIENCE],
	       scopes=[endpoints.EMAIL_SCOPE])
class Tyndr_API(remote.Service):
	""" Tyndr API v1. """
	
	CREATE = endpoints.ResourceContainer(CreateAdvertMessage)
	@endpoints.method(CREATE,
			  StatusMessage,
			  path='create',
			  http_method='POST',
			  name='advert.create')
	def create_advert(self, request):
		""" Grabs information from the request.POST and populates
		an Advert instance with it.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		# TODO:
		#category = request.get('advert_category', LOST_PETS)
		category = LOST_PETS
		user = endpoints.get_current_user()
		#if not user:
		#	return StatusMessage(message='unidentified user: %s' % (user,))
		# Create a new advert
		advert = Advert(parent = adverts_key(category),
				author = user,
				name = request.name,
				description = request.description)
		advert.put()
		return StatusMessage(message='success')


	NO_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			no = messages.IntegerField(1, variant=messages.Variant.INT32))
	@endpoints.method(NO_RESOURCE,
			  AdvertMessageCollection,
			  path='all/{no}',
			  http_method='GET',
			  name='advert.all')
	def get_all_adverts(self, request):
		""" Currently returns the no newest adverts in Datastore.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		# TODO:
		#category = request.get('advert_category', LOST_PETS)
		category = LOST_PETS
		adverts = Advert.query(ancestor=adverts_key(category))\
				.order(-Advert.date_created)
		adverts = adverts.fetch(request.no)
		# Package adverts in messages
		result = [AdvertMessage(id = ad.key.id(),
					author = str(ad.author),
					name = ad.name,
					description = ad.description,
					date_created = ad.date_created)
			  for ad in adverts]
		return AdvertMessageCollection(items=result)
	
	ID_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			id = messages.IntegerField(1, variant=messages.Variant.INT32))
	@endpoints.method(ID_RESOURCE,
			  AdvertMessage,
			  path='single/{id}',
			  http_method='GET',
			  name='advert.query')
	def query_adverts(self, request):
		""" Returns the Advert with id.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		print("Requested ad: " + str(request.id))
		try:
			# Query on ancestor
			ad = ndb.Key('AdvertCategory',
				     LOST_PETS,
				     'Advert',
				     request.id).get()
			return AdvertMessage(id = ad.key.id(),
					     author = str(ad.author),
					     name = ad.name,
					     description = ad.description,
					     date_created = ad.date_created)
		except Exception as e:
			print(e)
			raise endpoints.NotFoundException(
					'Advert %s not found.' % (request.id,))

APPLICATION = endpoints.api_server([Tyndr_API])
