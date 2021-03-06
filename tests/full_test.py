import requests, json, pprint
import time


def full_test(username, password):
    """register part"""
    url = 'http://127.0.0.1:5000/register'

    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {'username': username, 'password': password}

    # we convert dict to json string by json.dumps()
    resp = requests.post(url, headers=headers, data=json.dumps(payload))

    # this assertion means that this user already exists in api's database
    print(resp)
    # assert resp.status_code == 201

    # print response full body as text
    if resp.status_code == 201:
        print(resp.text)
    else:
        # <Response [400]>
        print("User already exists")


    """token part"""
    url = 'http://127.0.0.1:5000/gettoken'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))

    assert resp.status_code == 201

    # we get the token
    token = resp.json()['token']
    print()
    print(token)


    """path part"""
    # if we wait more than 30 sec token will expire and we'll get 'Unauthorized Access' message
    # time.sleep(34)
    # now we have token, we can ask for the path
    url = 'http://127.0.0.1:5000/stops'

    # password is None because we already have a token
    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(token, None))
    print()
    print(resp.text)

    url = 'http://127.0.0.1:5000/path'

    # find a path example
    payload = {'source': 1,
               'target': 29}
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    print()
    pprint.pprint(resp.text)

    # when the source is the target
    payload = {'source': 1,
               'target': 1}
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    print()
    pprint.pprint(resp.text)

    # when one of the stops doesn't exist
    payload = {'source': 1,
               'target': 42}
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    print()
    pprint.pprint(resp.text)

    # when the payload is incomplete
    payload = {'source': 1}
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    print()
    # <Response [500]>
    # print(resp)
    pprint.pprint(resp.text)


full_test('fulluzytkownik', 'jegofullhaslo')

"""
user = input()
pwd = input()
full_test(user, pwd)
"""
