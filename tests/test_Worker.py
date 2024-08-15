import unittest
from Worker import Worker

class TestWorker(unittest.TestCase):
    
    USERID = 'test'
    
    def setUp(self):
        self.worker = Worker()
    
    def test_0_newRequest(self):
        response = self.worker.new_request.delay(self.USERID, True)
        pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        self.assertRegex(response.id, pattern)
        
    def test_1_newRequest(self):
        response = self.worker.new_request(self.USERID, True)
        self.assertEqual(response['progress'], 100)