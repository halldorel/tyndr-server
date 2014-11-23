from google.appengine.ext import ndb


class Advert(ndb.Model):
    """ Models an individual Advert.

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
    author = ndb.UserProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty(indexed = False)
    species = ndb.StringProperty()
    subspecies = ndb.StringProperty(default = None)
    color = ndb.StringProperty()
    age = ndb.IntegerProperty()
    lat = ndb.FloatProperty()
    lon = ndb.FloatProperty()
    date_created = ndb.DateTimeProperty(auto_now_add = True)
    resolved = ndb.BooleanProperty(default = False)


class Picture(ndb.Model):
    """ An uploaded picture.

    Author: Halldor Eldjarn, hae28@hi.is """
    author = ndb.UserProperty()
    location = ndb.GeoPtProperty()
    date_uploaded = ndb.DateTimeProperty(auto_now_add = True)
    picture_data = ndb.BlobProperty()
    advert_id = ndb.IntegerProperty()


#class Conversation(ndb.Model):
#	""" Represents a collection of messages between 2+ users
#
#	Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
#	parties = ndb.KeyProperty(kind = 'User', repeated = True)
#

class Message(ndb.Model):
    """ A single message between two users

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
    text = ndb.StringProperty(indexed = False)
    sender = ndb.UserProperty()
    receiver = ndb.UserProperty()
    date_created = ndb.DateTimeProperty(auto_now_add = True)
    seen = ndb.DateTimeProperty(indexed = False)


# Advert collections should be queried on their common ancestor
def adverts_key(advert_category):
    """ Constructs a Datastore key for Advert Category entity with
    category name advert_category.

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
    Params:
        advert_category: String, key for an AdvertCategory in
        the Datastore. """
    return ndb.Key('AdvertCategory', advert_category)
