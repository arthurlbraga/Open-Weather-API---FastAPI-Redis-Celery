import unittest
from OpenWeatherAPI import OpenWeatherAPI
from Utils import Utils

class TestFastAPI(unittest.TestCase):
    
    CITYIDS = Utils.CITY_IDS_TEST
    
    def setUp(self):
        self.owAPI = OpenWeatherAPI()
    
    def test_0_getWeather(self):
        response = self.owAPI.get_current_weather(self.CITYIDS[0])
        self.assertEqual(response["id"], self.CITYIDS[0])
        self.assertTrue("weather" in response)
        
    def test_1_checkUnexistingCity(self):
        unexistingId = 1000000
        response = self.owAPI.get_current_weather(unexistingId)
        self.assertEqual(response, 404)