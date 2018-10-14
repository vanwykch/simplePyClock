import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
import json
import oauth2


CLIENT_ID = '22D7JS'
CLIENT_SECRET = '88602d8c5d5872b3905c4828cce68333'
redirect_uri='http://127.0.0.1:8080/'
class ctv_date:
	year = '2018'
	month = '09'
	day = '30'

ACCESS_TOKEN = 'no access'
REFRESH_TOKEN = 'no refesh'
f = open( 'auth', 'r' )
lines = f.readlines()
ACCESS_TOKEN =	lines[0]
REFRESH_TOKEN = lines[1]
f.close()

print (ACCESS_TOKEN)
print('\n')
print (REFRESH_TOKEN)


server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
print ACCESS_TOKEN
print REFRESH_TOKEN
f = open( 'auth', 'w' )
f.write('\n\n')
f.write(ACCESS_TOKEN)
f.write('\n\n')
f.write(REFRESH_TOKEN)
f.write('\n\n')
f.close()
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, redirect_uri=redirect_uri, timeout=10)
today = datetime.date.today().strftime('%Y-%m-%d')

sleep = auth2_client.get_sleep(ctv_date)
f = open( 'sleep.json', 'w' )
f.write( json.dumps(sleep, indent=4, sort_keys=True) )
hours_sleep = sleep['summary']['totalMinutesAsleep'] / 60.0
print(sleep['summary']['stages']['wake'] )
print(sleep['summary']['stages']['deep'] )
print(sleep['summary']['stages']['light'] )
print(hours_sleep)
f.close()

