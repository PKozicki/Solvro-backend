import requests
import json


def test_gettoken(username, password):
    url = 'http://127.0.0.1:5000/gettoken'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))

    assert resp.status_code == 200
    print(resp)

    # print response body as text
    print(resp.text)


test_gettoken('uzytkownik', 'jegohaslo')
