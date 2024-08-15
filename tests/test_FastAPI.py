import unittest
from fastapi.testclient import TestClient
from main import app
from time import sleep

class TestFastAPI(unittest.TestCase):
    
    USERID = 'test'
    
    def setUp(self):
        self.client = TestClient(app)
    
    def test_0_serviceOnline(self):
        response = self.client.get("/")
        json_response = response.json()
        self.assertEqual(json_response, {"INFO": "You can use this API by sending a POST request containing the following body: {'userId': '<userID>'}. Additionally you can track requests for created users by sending a GET request to /<userID>"})
    
    def test_1_checkPayload(self):
        payload = {}
        response = self.client.post("/", json=payload)
        json_response = response.json()
        self.assertEqual(json_response, {"ERROR": "No userId provided in the payload"})
    
    def test_2_getUnknownUserProgress(self):
        response = self.client.get(f"/{self.USERID}")
        json_response = response.json()
        self.assertEqual(json_response, {"ERROR": "The User ID informed doesn't exist in our database"})
    
    def test_3_newRequest(self):
        payload = {
            "userId": self.USERID
        }
        response = self.client.post("/", json=payload)
        json_response = response.json()["INFO"]
        pattern = r"New request created with TaskID = [0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        self.assertRegex(json_response, pattern)
        
    def test_4_getProgress(self):
        response = self.client.get(f"/{self.USERID}")
        json_response = response.json()["INFO"]
        pattern = r"The request for this user is being processed\. Status = \d+%"
        self.assertRegex(json_response, pattern)
        sleep(10)
        response = self.client.get(f"/{self.USERID}")
        json_response = response.json()["INFO"]
        pattern = r"Status = \d+%"
        self.assertRegex(json_response, pattern)
        
    def test_5_getFavicon(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "image/vnd.microsoft.icon")