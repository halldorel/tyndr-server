""" Back end for Tyndr implemented using Google Cloud Endpoints.
"""

import endpoints
# Message passing
from protorpc import messages
from protorpc import message_types
from protorpc import remote

# Database access
from google.appengine.api import users
from google.appengine.ext import ndb

WEB_CLIENT_ID = ''
ANDROID_CLIENT_ID = ''
IOS_CLIENT_ID = ''
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'tyndr-server'

# Default advert categories
FOUND_PETS = 'found_pets'
LOST_PETS = 'lost_pets'

# Advert collections should be queried on their common ancestor
def adverts_key(advert_category=FOUND_PETS):
	""" Constructs a Datastore key for Advert Category entity with
	category name advert_category.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is 
	Params:
		advert_category: String, key for an AdvertCategory in
		the Datastore. """
	return ndb.Key('AdvertCategory', advert_category)

# TODO:
# Move models into a separate package
class Advert(ndb.Model):
	""" Models an individual Advert. 
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	# TODO:
	#	Associate an Advert object with a User object
	#	Create user mgmt system
	#author = ndb.UserProperty()
	author = ndb.StringProperty()
	name = ndb.StringProperty()
	description = ndb.StringProperty(indexed = False)
	date_created = ndb.DateTimeProperty(auto_now_add = True)

class AdvertMessage(messages.Message):
	""" Contains information about a single advert.
	Used to pass model representations to a front end.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	author = messages.StringField(1)
	name = messages.StringField(2)
	description = messages.StringField(3)
	date_created = message_types.DateTimeField(4)

class AdvertMessageCollection(messages.Message):
	""" Collection of AdvertMessages. Used to pass multiple adverts
	to the front end.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	items = messages.MessageField(AdvertMessage, 1, repeated=True)

class StatusMessage(messages.Message):
	""" Passes status to front end when operation should not return
	another value.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	message = messages.StringField(1)



@endpoints.api(name='tyndr', version='v1')
class Tyndr_API(remote.Service):
	""" Tyndr API v1. """
	
	# EXPERIMENTALE LOCO
	# ==================
	CREATE = endpoints.ResourceContainer(
		 AdvertMessage)
		 
	@endpoints.method(CREATE,
			  StatusMessage,
			  path='advert',
			  http_method='POST',
			  name='advert.create')
	def create_advert(self, request):
		""" Grabs information from the request.POST and populates
		an Advert instance with it.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		# TODO:
		#category = request.get('advert_category', LOST_PETS)
		category = LOST_PETS
		# Create a new advert
		advert = Advert(parent = adverts_key(category),
				author = request.author,
				name = request.name,
				description = request.description)
		advert.put()
		#print(advert.id)
		return StatusMessage(message='success')

	NO_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			no = messages.IntegerField(1, variant=messages.Variant.INT32))
	@endpoints.method(NO_RESOURCE,
			  AdvertMessageCollection,
			  path='advert/all/{no}',
			  http_method='GET',
			  name='advert.all')
	def get_all_adverts(self, request):
		print("here")
		""" Currently returns the no newest adverts in Datastore.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		# TODO:
		#category = request.get('advert_category', LOST_PETS)
		category = LOST_PETS
		print(request.no)
		adverts = Advert.query(ancestor=adverts_key(category))\
				.order(-Advert.date_created)
		adverts = adverts.fetch(request.no)
		print(adverts)
		# Package adverts in messages
		result = [AdvertMessage(author = ad.author,
					name = ad.name,
					description = ad.description,
					date_created = ad.date_created)
			  for ad in adverts]
		return AdvertMessageCollection(items=result)
	"""	
	@endpoints.method(message_types.VoidMessage,
			  StatusMessage,
			  path='advert/{number}',
			  http_method='GET',
			  name='advert.test')
	def test_ads(self, request):
		return StatusMessage(message = 'test')
		category = LOST_PETS
		adverts = Advert.query(ancestor=adverts_key(category))\
				.order(-Advert.date_created)
		adverts = adverts.fetch(request.number)
		# Package adverts in messages
		result = [AdvertMessage(author = ad.author,
					name = ad.name,
					description = ad.description,
					date_created = ad.date_created)
			  for ad in adverts]
		return AdvertMessageCollection(items=result)
	"""
	"""
	@endpoints.method(message_types.VoidMessage, StatusMessage,
			path='advert/weird', http_method='GET',
			name='advert.test')
	def greetings_list(self, unused_request):
		return StatusMessage(message = 'test')
	"""
	ID_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			id = messages.IntegerField(1, variant=messages.Variant.INT32))
	@endpoints.method(ID_RESOURCE,
			  AdvertMessage,
			  path='advert/{id}',
			  http_method='GET',
			  name='advert.query')
	def query_adverts(self, request):
		""" Returns the Advert with id.
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		try:
			ad = Advert.get_by_id(request.id)
			return AdvertMessage(author = ad.author,
					     name = ad.name,
					     description = ad.description,
					     date_created = ad.date_created)
		except Exception as e:
			print(e)
			raise endpoints.NotFoundException('Advert %s not found.' % (request.id,))


	# EXPERIMENTO LOCO EST FINITO
	# ===========================


APPLICATION = endpoints.api_server([Tyndr_API])
