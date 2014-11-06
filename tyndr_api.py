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

def pack_adverts(adverts):
	result = [AdvertMessage(id = ad.key.id(),
				author = str(ad.author),
				name = ad.name,
				description = ad.description,
				species = ad.species,
				subspecies = ad.subspecies,
				color = ad.color,
				age = ad.age,
				date_created = ad.date_created)
		  for ad in adverts]
	return AdvertMessageCollection(items=result)

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
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
		Author: Halldor Eldjarn, hae28@hi.is """
		label = request.label if request.label else LOST_PETS
		user = endpoints.get_current_user()
		#if not user:
		#	return StatusMessage(message='unidentified user: %s' % (user,))
		# Create a new advert
		advert = Advert(parent = adverts_key(label),
				author = user,
				name = request.name,
				description = request.description,
				species = request.species,
				subspecies = request.subspecies,
				age = request.age)
		advert.put()
		return StatusMessage(message='success')


	NO_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			no = messages.IntegerField(1, variant=messages.Variant.INT32),
			label = messages.StringField(2, variant=messages.Variant.STRING))
	@endpoints.method(NO_RESOURCE,
			  AdvertMessageCollection,
			  path='all/{no}',
			  http_method='GET',
			  name='advert.all')
	def get_all_adverts(self, request):
		""" Currently returns the no newest adverts in Datastore.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		label = request.label if request.label else LOST_PETS
		adverts = Advert.query(ancestor=adverts_key(label))\
				.order(-Advert.date_created)
		adverts = adverts.fetch(request.no)
		# Package adverts in messages
		return pack_adverts(adverts)

	ID_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			id = messages.IntegerField(1, variant=messages.Variant.INT32),
			label = messages.StringField(2, variant=messages.Variant.STRING))
	@endpoints.method(ID_RESOURCE,
			  AdvertMessage,
			  path='single/{id}',
			  http_method='GET',
			  name='advert.query')
	def query_adverts(self, request):
		""" Returns the Advert with id.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
		Author: Halldor Eldjarn, hae28@hi.is """
		print("Requested ad: " + str(request.id))
		label = request.label if request.label else LOST_PETS
		try:
			# Query on ancestor
			ad = ndb.Key('AdvertCategory',
				     label,
				     'Advert',
				     request.id).get()
			return AdvertMessage(id = ad.key.id(),
					     author = str(ad.author),
					     name = ad.name,
					     description = ad.description,
					     species = ad.species,
					     subspecies = ad.subspecies,
					     color = ad.color,
					     age = ad.age,
					     date_created = ad.date_created)
		except Exception as e:
			print(e)
			raise endpoints.NotFoundException(
					'Advert %s not found.' % (request.id,))
	
	@endpoints.method(message_types.VoidMessage,
			  AdvertMessageCollection,
			  path='my-ads',
			  http_method='GET',
			  name='advert.mine')
	def get_my_adverts(self, request):
		""" Returns an AdvertMessageCollection of all of an
		authorised user's Adverts.

		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		user = endpoints.get_current_user()
		adverts = Advert.query(Advert.user = user)
		return pack_adverts(adverts)


APPLICATION = endpoints.api_server([Tyndr_API])
