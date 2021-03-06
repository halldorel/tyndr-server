""" Back end for Tyndr implemented using Google Cloud Endpoints.

M: models.py
V: tyndr_api.py
C: messages.py
"""

package = 'tyndr-server'

import endpoints
# Message passing
from protorpc import remote

# Utils
from methods import *

WEB_CLIENT_ID = '259192441078-gmov6a7cj5dbg8ikdgkdalht3vuevs00.apps.googleusercontent.com'
ANDROID_CLIENT_ID = '259192441078-65b660d346mf6sirs2mpcbg03sdk8ftj.apps.googleusercontent.com'
IOS_CLIENT_ID = ''
ANDROID_AUDIENCE = WEB_CLIENT_ID


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


    #################
    #               #
    #    ADVERTS    #
    #               #
    #################

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
        if user is None:
            raise endpoints.UnauthorizedException('Invalid token')
        # Create a new advert
        advert = Advert(
            parent = adverts_key(label),
            author = user,
            name = request.name,
            description = request.description,
            species = request.species,
            subspecies = request.subspecies,
            color = request.color,
            age = request.age,
            lat = request.lat,
            lon = request.lon,
            sex = request.sex,
            fur = request.fur,
            image = request.image_string
        )
        reference = str(advert.put().id())

        return AdvertReferenceMessage(reference=reference)


    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1, variant=messages.Variant.STRING),
        label=messages.StringField(2, variant=messages.Variant.STRING)
    )

    @endpoints.method(ID_RESOURCE,
                      AdvertMessage,
                      path='single/{id}',
                      http_method='GET',
                      name='advert.query')
    def query_adverts(self, request):
        """ Returns the Advert with id.

        Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is
        Author: Halldor Eldjarn, hae28@hi.is """
        logging.info("Requested ad: " + str(request.id))
        label = request.label if request.label else LOST_PETS
        try:
            ad = query_ad(label, request.id)
            user = endpoints.get_current_user()
            return AdvertMessage(id = ad.key.id(),
                                 author = str(ad.author),
                                 author_name = ad.author.nickname() if ad.author else '',
                                 author_email = ad.author.email() if ad.author else '',
                                 name = ad.name,
                                 description = ad.description,
                                 species = ad.species,
                                 subspecies = ad.subspecies,
                                 color = ad.color,
                                 age = ad.age,
                                 lat = ad.lat,
                                 lon = ad.lon,
                                 sex = ad.sex,
                                 fur = ad.fur,
                                 date_created = ad.date_created,
                                 resolved = ad.resolved,
                                 mine = ad.author == user,
                                 image_string = ad.image)
        except Exception as e:
            logging.info(e)
            raise endpoints.NotFoundException(
                'Advert %s not found.' % (request.id,)
            )


    @endpoints.method(ID_RESOURCE,
                      AdvertMessage,
                      path='image/{id}',
                      http_method='GET',
                      name='advert.img')
    def get_ad_img(self, request):
        label = request.label if request.label else LOST_PETS
        try:
            ad = query_ad(label, request.id)
            return AdvertMessage(id = ad.key.id(),
                                 image_string = ad.image)
        except Exception as e:
            logging.info(e)
            raise endpoints.NotFoundException(
                'Advert %s not found.' % (request.id,)
            )


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
        if user is None:
            raise endpoints.UnauthorizedException('Invalid token')
        try:
            ad = query_ad(label, request.id)
            if ad.user != user:
                return StatusMessage(message='illegal')
            ad.resolved = True
            ad.put()
            return StatusMessage(message='success')

        except Exception as e:
            logging.info(e)
            raise endpoints.NotFoundException(
                'Advert $s not found.' % (request.id))


    NO_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        no=messages.IntegerField(1, variant=messages.Variant.INT32),
        label=messages.StringField(2, variant=messages.Variant.STRING)
    )

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
        adverts = Advert.query(ancestor=adverts_key(label)) \
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
        if user is None:
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
        if user is None:
            raise endpoints.UnauthorizedException('Invalid token')
        return StatusMessage(message=user.email())

    LOC_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        lat = messages.FloatField(1, variant = messages.Variant.DOUBLE),
        lon = messages.FloatField(2, variant = messages.Variant.DOUBLE),
        rng = messages.FloatField(3, variant = messages.Variant.DOUBLE),
        label = messages.StringField(4, variant = messages.Variant.STRING)
    )

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
        rng = request.rng if request.rng else 0.2

        label = request.label if request.label else LOST_PETS
        ads = get_ads_in_range(label, lat, lon, rng)
        return pack_adverts(ads)


APPLICATION = endpoints.api_server([Tyndr_API])