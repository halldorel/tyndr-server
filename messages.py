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
	name = messages.StringField(3)
	description = messages.StringField(4)
	species = messages.StringField(5)
	subspecies = messages.StringField(6)
	color = messages.StringField(7)
	age = messages.IntegerField(8)
	date_created = message_types.DateTimeField(9)
	# Geotag
	lat = messages.FloatField(10)
	lon = messages.FloatField(11)
	resolved = messages.BooleanField(12)

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

class StatusMessage(messages.Message):
	""" Passes status to front end when operation should not return
	another value.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	message = messages.StringField(1)

class AdvertReferenceMessage(messages.Message):
	""" Passes an advert's reference number to the endpoint
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	reference = messages.StringField(1)

class UploadPictureMessage(messages.Message):
	""" Passes info with uploaded Picture.

	Author: Halldor Eldjarn, hae28@hi.is """
	lat = messages.FloatField(1)
	lon = messages.FloatField(2)
