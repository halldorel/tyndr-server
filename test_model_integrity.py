import unittest
import time

from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from models import *

class ModelTestCase(unittest.TestCase):
    """ Basic tests for Model integrity

    Author: Kristjan ELdjarn Hjorleifsson, keh4@hi.is """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Create a consistency policy that will simulate the HRD consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=0)
        # Initialize stub with said policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_hrd_writes(self):
        """ Tests the consistency policy of the HRD. """

        class TestModel(ndb.Model):
            pass

        user_key = ndb.Key.from_path('User', 'kristjan')
        # Put two entities
        ndb.put([TestModel(parent=user_key),
                 TestModel(parent=user_key)])

        # Global query shouldn't see the data, as per HRD consistency policy
        self.assertEqual(0, TestModel.query().fetch().count(3))
        # Ancestor query should see the data
        # => Hence, we do all our other queries on ancestor
        self.assertEqual(2, TestModel.query().fetch().ancestor(user_key).count(3))


    def test_model_creation(self):
        """ Tests the creation of a single advert, with time constraints. """

        key = 'lost_pets'
        start = time.time()

        ad = Advert(parent = adverts_key(key),
                    author = None,
                    name = 'Tommi',
                    description = 'Tall, blond',
                    species = 'Human',
                    subspecies = 'Homo sapiens',
                    color = 'white',
                    age = '23',
                    lat = 100.0,
                    lon = -27.0)
        key = ad.put()
        reference = key.id()

        # If the put() method is blocking, ad.date_created should be in the
        # range [start; end]
        end = time.time()

        # Query the datastore for the created model:
        ad = ndb.Key('AdvertCategory',
                     key,
                     'Advert',
                     reference).get()

        self.assertEqual(ad.name, 'Tommi')
        # Time constraints
        self.assertTrue(ad.date_created > start)
        self.assertTrue(ad.date_created < end)







unittest.main()