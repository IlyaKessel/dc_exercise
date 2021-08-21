from django.test import TestCase
import requests_mock

mock_session = requests_mock.Mocker()
class DetectionsTest(TestCase):
   
    def setUp(self):
        mock_session.register_uri('POST', 
                                 'https://postman-echo.com/post',
                                 headers={'Content-Type': 'application/json'},
                                 json={
                                        "args": {},
                                        "data": "Mike's laptop of this mike (242-22-5322) (111111111) (130964321) patch can not be applied in the last week ****.",
                                        "files": {},
                                        "form": {},
                                        "headers": {
                                            "x-forwarded-proto": "https",
                                            "x-forwarded-port": "443",
                                            "host": "localhost",
                                            "x-amzn-trace-id": "Root=1-6121539b-05188b7f7aeb49c239b62f59",
                                            "content-length": "123",
                                            "user-agent": "PostmanRuntime/7.26.2",
                                            "accept-encoding": "gzip, deflate, br",
                                            "accept": "*/*",
                                            "content-type": "text/plain",
                                            "cache-control": "no-cache",
                                            "postman-token": "c98af1a3-d3fa-46a2-8b24-fb210d1ad8ff"
                                        },
                                        "json": None,
                                        "url": "https://localhost/post"
                                    })
    def test_mask(self):

        mock_session.start()
        resp = self.client.post('/post',
                                headers={'Content-type': 'application/json'},
                                data={"t": "Mike The laptop of Mike Mike's  (242-22-5322) (111111111) (130964321) patch can not be applied in the last week Mike."})
        
        text = resp.json()['data'].lower()
        self.assertEqual('mike' not in text, True)
        self.assertEqual('242-22-5322' in text, False)
        self.assertEqual('111111111' in text, True)
        self.assertEqual('130964321' in text, False)
        


       