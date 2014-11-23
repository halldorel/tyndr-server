""" Back end for Tyndr implemented using Google Cloud Endpoints.

M: models.py
V: tyndr_api.py
C: messages.py
"""

package = 'tyndr-server'

import endpoints
# Message passing
from protorpc import messages
from protorpc import message_types
from protorpc import remote

# Database access
from google.appengine.api import users
from google.appengine.ext import ndb

# Image handling
from google.appengine.api import images

# Models
from models import *
# Messages
from messages import *

WEB_CLIENT_ID = ''
ANDROID_CLIENT_ID = ''
IOS_CLIENT_ID = ''
ANDROID_AUDIENCE = WEB_CLIENT_ID

LAT_R = 0.2
LON_R = 0.2

# Default advert categories
FOUND_PETS = 'found_pets'
LOST_PETS = 'lost_pets'

def pack_adverts(adverts):
	""" Packs adverts in an AdvertMessageCollection

	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
	Params:
		adverts: A list of Advert model instances. """
	result = [AdvertMessage(id = ad.key.id(),
				author = str(ad.author),
				name = ad.name,
				description = ad.description,
				species = ad.species,
				subspecies = ad.subspecies,
				color = ad.color,
				age = ad.age,
				lat = ad.lat,
				lon = ad.lon,
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
			  AdvertReferenceMessage,
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
		#if user is None:
		#	raise endpoints.UnauthorizedException('Invalid token')
		# Create a new advert
		advert = Advert(parent = adverts_key(label),
				author = user,
				name = request.name,
				description = request.description,
				species = request.species,
				subspecies = request.subspecies,
				color = request.color,
				age = request.age,
				lat = request.lat,
				lon = request.lon)
		reference = str(advert.put().id())
		
		return AdvertReferenceMessage(reference = reference)

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
					     lat = ad.lat,
					     lon = ad.lon,
					     date_created = ad.date_created,
					     resolved = ad.resolved)
		except Exception as e:
			print(e)
			raise endpoints.NotFoundException(
					'Advert %s not found.' % (request.id,))
	
	
	@endpoints.method(ID_RESOURCE,
			  StatusMessage,
			  path='resolve/{id}',
			  http_method='POST',
			  name='advert.resolve')
	def resolve_advert(self, request):
		""" If the invoking user is the owner of advert, it is 
		marked as resolved

		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		label = request.label if request.label else LOST_PETS
		user = endpoints.get_current_user()
		if raise_unauthorized and current_user is None:
			raise endpoints.UnauthorizedException('Invalid token')
		try:
			ad = ndb.Key('AdvertCategory',
				     label,
				     'Advert',
				     request.id).get()
			if ad.user != user:
				return StatusMessage(message = 'illegal')
			ad.resolved = True
			ad.put()
			return StatusMessage(message = 'success')

		except Exception as e:
			print(e)
			raise endpoints.NotFoundException(
					'Advert $s not found.' % (request.id))

		

	#UPLOAD_PICTURE = endpoints.ResourceContainer(UploadImageMessage)
	#@endpoints.method(UPLOAD_PICTURE,
	#	UploadPictureMessage,
	#	path='upload',
	#	http_method='POST',
	#	name='picture.create')
	#def upload_picture(self, request):
	#	""" Uploads the image from the request to the S3 bucket. 
	#
	#	Author: Halldor Eldjarn, hae28@hi.is
	#	"""
	#	# TODO:  Should upload image data to S3 instead of storing in db
	#
	#	picture_data = request.get('picture')
	#
	#	user = endpoints.get_current_user()
	#	location = GeoPt(request.lat, request.lon)
	#	picture = Picture(author = user,
	#		location = location,
	#		picture_data = db.Blob(picture_data))
	#	picture.put()
	#	return StatusMessage(message='success')

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
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
		Author: Halldor Eldjarn, hae28@hi.is """
		label = request.label if request.label else LOST_PETS
		adverts = Advert.query(ancestor=adverts_key(label))\
				.order(-Advert.date_created)
		adverts = adverts.fetch(request.no)
		# Package adverts in messages
		return pack_adverts(adverts)
	
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
		if raise_unauthorized and current_user is None:
			raise endpoints.UnauthorizedException('Invalid token')
		adverts = Advert.query(user == user)
		return pack_adverts(adverts)

	@endpoints.method(message_types.VoidMessage,
			  StatusMessage,
			  path='user-debug',
			  http_method='GET',
			  name='user.debug')
	def user_auth_debug(self, request):
		""" Returns the email address of authorised user 
		
		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		user = endpoints.get_current_user()
		if raise_unauthorized and current_user is None:
			raise endpoints.UnauthorizedException('Invalid token')
		return StatusMessage(message = user.email())

	LOC_RESOURCE = endpoints.ResourceContainer(
			message_types.VoidMessage,
			lat = messages.StringField(1, variant=messages.Variant.STRING),
			lon = messages.StringField(2, variant=messages.Variant.STRING),
			label = messages.StringField(3, variant=messages.Variant.STRING))
	@endpoints.method(LOC_RESOURCE,
			  AdvertMessageCollection,
			  path='loc-ads',
			  http_method='GET',
			  name='advert.loc')
	def get_adverts_by_location(self, request):
		""" Receives a latitude and a longitude and returns all adverts
		in a rectangular area around that location.

		Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
		lat = request.lat
		lon = request.lon

		label = request.label if request.label else LOST_PETS
		adverts = Advert.query(ancestor = adverts_key(label),
				       resolved == False,
				       lat > lat - LAT_R,
				       lat < lat + LAT_R,
				       lon > lon - LON_R,
				       lon < lon + LON_R)
		return pack_adverts(adverts)

APPLICATION = endpoints.api_server([Tyndr_API])
