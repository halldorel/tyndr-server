from google.appengine.ext import ndb

class Advert(ndb.Model):
	""" Models an individual Advert. 

	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
	# TODO:
	#	Associate an Advert object with a User object
	#	Create user mgmt system
	author = ndb.UserProperty()
	description = ndb.StringProperty()
	name = ndb.StringProperty()
	description = ndb.StringProperty(indexed = False)
	species = ndb.StringProperty()
	subspecies = ndb.StringProperty(default=None)
	color = ndb.StringProperty()
	date_created = ndb.DateTimeProperty(auto_now_add = True)


# Advert collections should be queried on their common ancestor
def adverts_key(advert_category):
	""" Constructs a Datastore key for Advert Category entity with
	category name advert_category.
	
	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is 
	Params:
		advert_category: String, key for an AdvertCategory in
		the Datastore. """
	return ndb.Key('AdvertCategory', advert_category)
