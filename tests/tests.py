import requests, json, unittest


class TestCases(unittest.TestCase):
    def test_register_new_user(self):
        url = 'http://127.0.0.1:5000/register'
        username = 'fulluzytkownik'
        password = 'jegofullhaslo'

        headers = {'Content-Type': 'application/json'}
        payload = {'username': username, 'password': password}
        resp = requests.post(url, headers=headers, data=json.dumps(payload))

        self.assertIn(resp.status_code, [201, 409])

    def test_possibilities(self):
        """get token"""
        url = 'http://127.0.0.1:5000/gettoken'
        resp = requests.get(url, auth=requests.auth.HTTPBasicAuth('fulluzytkownik', 'jegofullhaslo'))
        token = resp.json()['token']
        self.assertEqual(resp.status_code, 201)

        """get stops"""
        url = 'http://127.0.0.1:5000/stops'
        resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(token, None))
        self.assertEqual(resp.status_code, 200)

        """get path"""
        url = 'http://127.0.0.1:5000/path'
        payload = {'source': 1,
                   'target': 29}
        resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
        self.assertEqual(resp.status_code, 200)

        """when the source is the target"""
        payload = {'source': 1,
                   'target': 1}
        resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
        response = json.loads(resp.text)
        self.assertEqual(response[1], 200)

        """when one of the stops doesn't exist"""
        payload = {'source': 1,
                   'target': 54}
        resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
        response = json.loads(resp.text)
        self.assertEqual(response[0]['status'], {"1": "Missing data"})

        """when the payload is incomplete"""
        payload = {'source': 'Przystanek Zdenerwowany frontend developer'}
        resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()
