""" Tyndr-server
messages.py """

from protorpc import messages
from protorpc import message_types

class AdvertMessage(messages.Message):
	""" Contains information about a single advert.
	Used to pass model representations to a front end.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	id = messages.IntegerField(1)
	author = messages.StringField(2)
	author_name = messages.StringField(3)
	author_email = messages.StringField(4)
	name = messages.StringField(5)
	description = messages.StringField(6)
	species = messages.StringField(7)
	subspecies = messages.StringField(8)
	color = messages.StringField(9)
	age = messages.IntegerField(10)
	date_created = message_types.DateTimeField(11)
	# Geotag
	lat = messages.FloatField(12)
	lon = messages.FloatField(13)
	resolved = messages.BooleanField(14)
	# Denotes whether the querying client owns the advert
	mine = messages.BooleanField(15)
	# Image contains a blob representation of the related image
	image_string = messages.BytesField(16)

class AdvertMessageCollection(messages.Message):
	""" Collection of AdvertMessages. Used to pass multiple adverts
	to the front end.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	items = messages.MessageField(AdvertMessage, 1, repeated=True)

class CreateAdvertMessage(messages.Message):
	""" Passes information about a new ad from the endpoint
	to the backend.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	name = messages.StringField(1)
	description = messages.StringField(2)
	species = messages.StringField(3)
	subspecies = messages.StringField(4)
	color = messages.StringField(5)
	age = messages.IntegerField(6)
	lat = messages.FloatField(7)
	lon = messages.FloatField(8)
	label = messages.StringField(9, required=True)
	image_string = messages.BytesField(10)

class StatusMessage(messages.Message):
	""" Passes status to front end when operation should not return
	another value.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	message = messages.StringField(1)

class AdvertReferenceMessage(messages.Message):
	""" Passes an advert's reference number and image upload url
	to the endpoint.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	reference = messages.StringField(1)

class UploadPictureMessage(messages.Message):
	""" Passes info with uploaded Picture.

	Author: Halldor Eldjarn, hae28@hi.is """
	lat = messages.FloatField(1)
	lon = messages.FloatField(2)
