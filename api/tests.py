import datetime
from random import randint
from django.shortcuts import reverse
from django.test import TestCase
from .serializers import EarthQuakeSerializer
from .functions import scraper, update_earthquake_model, init_data
from .models import EarthQuake


class TestFunctions(TestCase):

    def setUp(self):
        self.scraped_data = scraper()

    def test_scraper_result_len(self):
        self.assertEqual(len(self.scraped_data), 45)

    def test_scraper_data_content_type_roundomly(self):
        element_index = randint(0, len(self.scraped_data)-1)
        element = self.scraped_data[element_index]
        msg = '{} content type is not {}'
        self.assertIsInstance(element['origin_time'],
                              datetime.datetime,
                              msg.format('origin_time', 'datetime'))
        self.assertIsInstance(element['magnitude'],
                              float,
                              msg.format('magnigude', 'float'))
        self.assertIsInstance(element['latitude'],
                              float,
                              msg.format('latitude', 'float'))
        self.assertIsInstance(element['longitude'],
                              float,
                              msg.format('longitude', 'float'))
        self.assertIsInstance(element['depth'],
                              int,
                              msg.format('depth', 'int'))
        self.assertIsInstance(element['region'],
                              list,
                              msg.format('region', 'str'))

    def test_init_data(self):
            query_set_len_befor = len(EarthQuake.objects.all())
            init_data()
            query_set_len_after = len(EarthQuake.objects.all())
            self.assertEqual(query_set_len_befor, 0)
            self.assertEqual(query_set_len_after, 45)

    def test_update_earthquake_model(self):
        befor_update_query_set = EarthQuake.objects.all()
        init_data()
        update_earthquake_model()
        after_update_query_set = EarthQuake.objects.all()
        self.assertGreaterEqual(len(befor_update_query_set),
                                len(after_update_query_set))


class TestAllEarthQuakesView(TestCase):

    def setUp(self):
        init_data()

    def test_all_earthquakes_view_by_url(self):
        response = self.client.get('/api/all/')
        self.assertEqual(response.status_code, 200)

    def test_all_earthquakes_view_respnse_list_length(self):
        response = self.client.get('/api/all/')
        self.assertGreaterEqual(len(response.json()), 45)


class TestLastNEarthQuakeView(TestCase):

    def setUp(self):
        init_data()

    def test_last_n_earthquake_view_by_url(self):
        m = randint(0, len(EarthQuake.objects.all())-1)
        response = self.client.get('/api/last/%d/'%m)
        self.assertEqual(response.status_code, 200)

    def test_last_n_earthquake_view_response_content(self):
        query_set = EarthQuake.objects.all()
        # divided by 2(or whatever morethan 1)
        m = len(query_set)//2
        response = self.client.get('/api/last/{}/'.format(m))
        self.assertEqual(len(response.json()), m)
        # request with m > len(all_data)
        response = self.client.get('/api/last/{}/'.format(len(query_set)+1))
        self.assertEqual(len(response.json()), 45)


class TestMagnitudeView(TestCase):

    def setUp(self):
        init_data()

    def test_magnitude_gte_status_code(self):
        magnitude = randint(2, 12)
        response = self.client.get('/api/magnitude_gte/%d/'%magnitude)
        self.assertEqual(response.status_code, 200)
        # float magnitude
        magnitude = 3/1
        response = self.client.get('/api/magnitude_gte/{:.1f}/'.format(magnitude))
        self.assertEqual(response.status_code, 200)

    def test_magnitude_gte_response_content(self):
        response = self.client.get('/api/magnitude_gte/100/')
        self.assertEqual(len(response.json()), 0)
