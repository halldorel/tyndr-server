import unittest

from google.appengine.ext import testbed

from models import *
from methods import *

class UtilTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()

    def test_query_ad_returns_correct_advert(self):
        label = 'lost_pets'
        name = 'Tommi'
        ad = Advert(label=label,
                    name=name)
        reference = ad.put().id()
        ad = query_ad(label, reference)
        self.assertEqual(name, ad.name)

    def test_get_ads_in_range_returns_correct_set(self):
        label = 'found_pets'
        name = 'Palli'
        lat = 100.0
        lon = -27.0
        rng = 0.2

        Advert(label=label,
               name=name,
               lat=lat,
               lon=lon).put()

        ads = get_ads_in_range(label,
                               lat - rng/2,
                               lon - rng/2,
                               rng)

        self.assertEqual(name, ads[0].name)