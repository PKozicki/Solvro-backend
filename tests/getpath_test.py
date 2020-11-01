import requests
import json


def test_getpath(username, password):
    url = 'http://127.0.0.1:5000/gettoken'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200

    token = resp.json()['token']

    # now we have token, we can ask for the path
    url = 'http://127.0.0.1:5000/getpath'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps('dzien dobry'))
    print(resp.text)


test_getpath('majster', 'kozicki')
