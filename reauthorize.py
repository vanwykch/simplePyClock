#!/usr/bin/python2
import gather_keys_oauth2 as Oauth2
import datetime
import json
import oauth2

TOKEN_FILE_NAME = 'tokens'
CLIENT_ID = '22D7JS'
CLIENT_SECRET = '88602d8c5d5872b3905c4828cce68333'
redirect_uri='http://127.0.0.1:8080/'

ACCESS_TOKEN = 'no access'
REFRESH_TOKEN = 'no refesh'



def get_client_and_secret():
    with open('cred.json') as file:
        data = json.load(file)

    print('client: ' + data['client'])
    print('secret: ' + data['secret'])
    CLIENT_ID = data['client']
    CLIENT_SECRET = data['secret']


get_client_and_secret    
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

f = open( TOKEN_FILE_NAME, 'w' )
f.write(ACCESS_TOKEN)
f.write('\n')
f.write(REFRESH_TOKEN)
f.close()
