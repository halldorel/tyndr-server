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
	date_created = message_types.DateTimeField(5)

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
	age = messages.IntegerField(5)

class StatusMessage(messages.Message):
	""" Passes status to front end when operation should not return
	another value.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	message = messages.StringField(1)
