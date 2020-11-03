import requests, json


def test_getpath(username, password):
    url = 'http://127.0.0.1:5000/gettoken'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))

    assert resp.status_code == 200

    token = resp.json()['token']

    # now we have token, we can ask for the path
    url = 'http://127.0.0.1:5000/path'

    payload = {'source': 'Przystanek Zdenerwowany frontend developer',
               'target': 'Przystanek Odważny frontend developer'}
    # password value is None because we already have a token
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    assert resp.status_code == 200
    print(resp.text)


test_getpath('uzytkownik', 'jegohaslo')
