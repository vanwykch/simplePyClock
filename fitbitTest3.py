#!/usr/bin/python2
import fitbit
import datetime
import json
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import sys
import os
import base64

# my fitbit device id
DEVICE_VERSION = 'Charge 2'
deviceId = 'no id found'

# Use this URL to refresh the access token
TokenURL = "https://api.fitbit.com/oauth2/token"

# Get and write the tokens from here
IniFile = "tokens"

# From the developer site
CLIENT_ID = '22D7JS'
CLIENT_SECRET = '88602d8c5d5872b3905c4828cce68333'
redirect_uri = 'http://127.0.0.1:8080/'


class ctv_date:
    year = '2018'
    month = '10'
    day = '06'


# Some contants defining API error handling responses
TokenRefreshedOK = "Token refreshed OK"
ErrorInAPI = "Error when making API call that I couldn't handle"

# Get the config from the config file.  This is the access and refresh tokens


def GetConfig():
    print("Reading from the config file")

    # Open the file
    FileObj = open(IniFile, 'r')

    # Read first two lines - first is the access token, second is the refresh token
    AccToken = FileObj.readline()
    RefToken = FileObj.readline()

    # Close the file
    FileObj.close()

    # See if the strings have newline characters on the end.  If so, strip them
    if (AccToken.find("\n") > 0):
        AccToken = AccToken[:-1]
    if (RefToken.find("\n") > 0):
        RefToken = RefToken[:-1]

    # Return values
    return AccToken, RefToken


def WriteConfig(AccToken, RefToken):
    print("Writing new token to the config file")
    print("Writing this: " + AccToken + " and " + RefToken)

    # Delete the old config file
    os.remove(IniFile)

    # Open and write to the file
    FileObj = open(IniFile, 'w')
    FileObj.write(AccToken + "\n")
    FileObj.write(RefToken + "\n")
    FileObj.close()


# Make a HTTP POST to get a new
def GetNewAccessToken(RefToken):
    print("Getting a new access token")

    # Form the data payload
    BodyText = {'grant_type': 'refresh_token',
                'refresh_token': RefToken}
    # URL Encode it
    BodyURLEncoded = urllib.parse.urlencode(BodyText)
    print("Using this as the body when getting access token >>" + BodyURLEncoded)

    # Start the request
    tokenreq = urllib.request.Request(TokenURL, BodyURLEncoded)

# Make a HTTP POST to get a new
def GetNewAccessToken(RefToken):
    print("Getting a new access token")

    # Form the data payload
    BodyText = {'grant_type': 'refresh_token',
                'refresh_token': RefToken}

    # URL Encode it
    BodyURLEncoded = urllib.parse.urlencode(BodyText)
    print("Using this as the body when getting access token >>" + BodyURLEncoded)

    # Start the request
    tokenreq = urllib.request.Request(TokenURL, BodyURLEncoded)

    # Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    tokenreq.add_header('Authorization', 'Basic ' +
                        base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET))
    tokenreq.add_header('Content-Type', 'application/x-www-form-urlencoded')

    # Fire off the request
    try:
        tokenresponse = urllib.request.urlopen(tokenreq)

    # See what we got back.  If it's this part of  the code it was OK
        FullResponse = tokenresponse.read()

    # Need to pick out the access token and write it to the config file.  Use a JSON manipluation module
        ResponseJSON = json.loads(FullResponse)

    # Read the access token as a string
        NewAccessToken = str(ResponseJSON['access_token'])
        NewRefreshToken = str(ResponseJSON['refresh_token'])

        # Write the access token to the ini file
        WriteConfig(NewAccessToken, NewRefreshToken)
        print("New access token output >>> " + FullResponse)

    except urllib.error.URLError as e:
        # Gettin to this part of the code means we got an error
        print("An error was raised when getting the access token.  Need to stop here")
        print(e.code)
        print(e.read())
        sys.exit()


def writeJsonStringToFile(jsonString, jsonFile):
    j = json.loads(jsonString)
    with open(jsonFile, 'w') as outfile:
        json.dump(j, outfile, indent=4)

def getDevices():
    URL = "https://api.fitbit.com/1/user/-/devices.json"
    ok, out = MakeAPICall(
        URL, AccessToken, RefreshToken)
    return ok, out


def getAlarms():
    ALARMS_URL = "https://api.fitbit.com/1/user/-/devices/tracker/" + deviceId + "/alarms.json"
    ok, out = MakeAPICall(
        ALARMS_URL, AccessToken, RefreshToken)
    return ok, out


def addAlarm(**kwargs):
    ALARMS_URL = "https://api.fitbit.com/1/user/-/devices/tracker/" + deviceId + "/alarms.json"
#    ok, out = MakeAPICall(ALARMS_URL, AccessToken, RefreshToken, **kwargs)
    ok, out = MakeAPICall(ALARMS_URL, AccessToken, RefreshToken)
    return ok, out


def getProfile():
    # This is the Fitbit URL to use for the API call
    PROFILE_URL = "https://api.fitbit.com/1/user/-/profile.json"

    ok, out = MakeAPICall(
        PROFILE_URL, AccessToken, RefreshToken)
    return ok, out


# This makes an API call.  It also catches errors and tries to deal with them
#def MakeAPICall(InURL, AccToken, RefToken, **kwargs):
def MakeAPICall(InURL, AccToken, RefToken):
    # Start the request
    req = urllib.request.Request(InURL)

    # Add the access token in the header
    req.add_header('Authorization', 'Bearer ' + AccToken)

# add arguments
#    for key, value in kwargs.items(): 
#        req.add_header(key, value)

    try:
        response = urllib.request.urlopen(req)
        FullResponse = response.read()
        out = FullResponse.decode("utf-8")
        return True, out

    # Catch errors, e.g. A 401 error that signifies the need for a new access token
    except urllib.error.URLError as e:
        print("Got this HTTP error: " + str(e.code))
        HTTPErrorMessage = e.read()
        writeJsonStringToFile(HTTPErrorMessage, "error.json")
        print("This was in the HTTP error message: " + HTTPErrorMessage)
        print("e.code: " + str(e.code))
        # See what the error was
        if (e.code == 401) and (HTTPErrorMessage.find("expired_token") > 0):
            print("Getting new access token")
            GetNewAccessToken(RefToken)
            return False, TokenRefreshedOK

        # Return that this didn't work, allowing the calling function to handle it
        return False, ErrorInAPI


def CreateTokensFile():

    NewAccessToken = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1WDZHQkgiLCJhdWQiOiIyMkQ3SlMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM4ODg3MzY5LCJpYXQiOjE1Mzg4NTg1Njl9.H-WRCuJvAwX_bgl3NaOYXM35mKkoQBhzF7C1zMtYq_I'
    NewRefreshToken = 'c71772ff8c2e7f1d34cf5bd21474aaaba91b5c359257b1b978428c75560bd06a'
    WriteConfig(NewAccessToken, NewRefreshToken)


def getSleep():

    auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=AccessToken,
                                 refresh_token=RefreshToken, redirect_uri=redirect_uri, timeout=10)
    today = datetime.date.today().strftime('%Y-%m-%d')

    sleep = auth2_client.get_sleep(ctv_date)
    f = open('sleep.json', 'w')
    f.write(json.dumps(sleep, indent=4, sort_keys=True))
    f.close()
    hours_sleep = sleep['summary']['totalMinutesAsleep'] / 60.0
    print((sleep['summary']['stages']['wake']))
    print((sleep['summary']['stages']['deep']))
    print((sleep['summary']['stages']['light']))
    print(hours_sleep)


# Main part of the code
# Declare these global variables that we'll use for the access and refresh tokens
AccessToken = ""
RefreshToken = ""

print("Fitbit API Test Code")
# CreateTokensFile()

# Get the config
AccessToken, RefreshToken = GetConfig()

# Make the API call
ok, devices = getDevices()
devicesJson = json.loads(devices)
for device in devicesJson:
   if device['deviceVersion'] == DEVICE_VERSION:
      deviceId = device['id']

print("My device id: " + deviceId)
writeJsonStringToFile(devices, "devices.json")

ok, alarms = getAlarms()
writeJsonStringToFile(alarms, "alarms.json")

ok, setAlarmsResponse = addAlarm(time = '07:15-08:00', enabled = 'true', recurring = 'false', weekDays = 'SATURDAY,SUNDAY')

ok, alarms = getAlarms()
writeJsonStringToFile(alarms, "alarmsNew.json")

if not ok:
    if (devices == TokenRefreshedOK):
        print("Refreshed the access token.  Can go again")
    else:
        print(ErrorInAPI)
