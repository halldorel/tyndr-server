import logging
from models import *
from messages import *


def query_ad(label, reference):
    """ Queries the datastore for an Advert with label and reference

    :param label: One of: 'lost_pets', 'found_pets'
    :param reference: Unique reference number for ad
    :return: An Advert corresponding to label and reference

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
    logging.info(reference)
    logging.info(type(reference))
    return ndb.Key('AdvertCategory',
                   label,
                   'Advert',
                   int(reference)).get()


def get_ads_in_range(label, lat, lon, rng):
    """ Gets all Adverts in a geographical range

    :param label: One of: 'lost_pets', 'found_pets'
    :param lat: Latitude of range center
    :param lon: Longitude of range center
    :param rng: Radius of bounding square
    :return: AdvertMessageCollection containing all ads matching query

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """

    ads = Advert.query(ancestor = adverts_key(label)) \
                .filter(Advert.resolved == False) \
                .filter(Advert.lat > (lat - rng),
                        Advert.lat < (lat + rng))
    # Datastore only allows one inequality comparison per query.
    # Hence, we have to do this filtering ourselves:
    return [a for a in ads if
            a.lon > lon - rng and a.lon < lon + rng]


def pack_adverts(adverts, user = None):
    """ Packs adverts in an AdvertMessageCollection

    :param adverts: A list of Advert model instances.

    Author: Kristjan Eldjarn Hjorleifsson, keh4@hi.is """
    result = [AdvertMessage(id=ad.key.id(),
                            author=str(ad.author),
                            author_name = ad.author.nickname() if ad.author else '',
                            author_email = ad.author.email() if ad.author else '',
                            name=ad.name,
                            description=ad.description,
                            species=ad.species,
                            subspecies=ad.subspecies,
                            color=ad.color,
                            age=ad.age,
                            lat=ad.lat,
                            lon=ad.lon,
                            date_created=ad.date_created,
                            resolved=ad.resolved,
                            mine = ad.author == user)
              for ad in adverts]
    return AdvertMessageCollection(items=result)