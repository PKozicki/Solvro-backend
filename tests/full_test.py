import requests, json, pprint


def full_test(username, password):
    """register part"""
    url = 'http://127.0.0.1:5000/register'

    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {'username': username, 'password': password}

    # we convert dict to json string by json.dumps()
    resp = requests.post(url, headers=headers, data=json.dumps(payload))

    # this assertion means that this user already exists in api's database
    # assert resp.status_code == 201
    # print(resp)

    # print response full body as text
    if resp.status_code == 201:
        print(resp.text)
    else:
        print("User already exists")


    """token part"""
    url = 'http://127.0.0.1:5000/gettoken'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))

    assert resp.status_code == 200

    # we get the token
    token = resp.json()['token']


    """path part"""
    # now we have token, we can ask for the path
    url = 'http://127.0.0.1:5000/stops'

    resp = requests.get(url, auth=requests.auth.HTTPBasicAuth(token, None))
    print()
    pprint.pprint(resp.text)

    url = 'http://127.0.0.1:5000/path'

    payload = {'source': 'Przystanek Zdenerwowany frontend developer',
               'target': 'Przystanek Odważny frontend developer'}
    resp = requests.post(url, auth=requests.auth.HTTPBasicAuth(token, None), data=json.dumps(payload))
    print()
    pprint.pprint(resp.text)


full_test('fulluzytkownik', 'jegofullhaslo')

"""
user = input()
pass = input()
full_test(user, pass)
"""
