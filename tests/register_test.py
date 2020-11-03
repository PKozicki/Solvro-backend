import requests
import json


def test_register(username, password):
    url = 'http://127.0.0.1:5000/register'

    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {'username': username, 'password': password}

    # convert dict to json string by json.dumps()
    resp = requests.post(url, headers=headers, data=json.dumps(payload))

    assert resp.status_code == 201
    print(resp)

    # print response body as text
    print(resp.text)


test_register('uzytkownik', 'jegohaslo')
