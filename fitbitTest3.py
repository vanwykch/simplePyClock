#!/usr/bin/python2
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
IniFile = "tokens.txt"

# From the developer site
CLIENT_ID = '22D7JS'
CLIENT_SECRET = '88602d8c5d5872b3905c4828cce68333'
redirect_uri = 'http://127.0.0.1:8080/'


class MyDate:
    year = '2018'
    month = '10'
    day = '06'


# Some constants defining API error handling responses
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
    file_obj = open(IniFile, 'w')
    file_obj.write(AccToken + "\n")
    file_obj.write(RefToken + "\n")
    file_obj.close()


def get_new_access_token(token):
    print("Getting a new access token")

    # Form the data payload
    body_text = {'grant_type': 'refresh_token', 'refresh_token': token}

    # URL Encode it
    body_encoded = urllib.parse.urlencode(body_text)
    print("Using this as the body when getting access token >>" + body_encoded)

    # Start the request
    token_request_response = urllib.request.Request(TokenURL, body_encoded)

    # Add the headers, first we base64 encode the client id and client secret with a ":"
    #  in between and create the authorisation header
    token_request_response.add_header('Authorization', 'Basic ' + base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET))
    token_request_response.add_header('Content-Type', 'application/x-www-form-urlencoded')

    # Fire off the request
    try:
        token_response = urllib.request.urlopen(token_request_response)

    # See what we got back.  If it's this part of  the code it was OK
        full_response = token_response.read()

    # Need to pick out the access token and write it to the config file.  Use a JSON manipluation module
        response_json = json.loads(full_response)

    # Read the access token as a string
        new_access_token = str(response_json['access_token'])
        new_refresh_token = str(response_json['refresh_token'])

        # Write the access token to the ini file
        WriteConfig(new_access_token, new_refresh_token)
        print("New access token output >>> " + full_response)

    except urllib.error.URLError as e:
        print("An error was raised when getting the access token.  Need to stop here")
        print(e.reason)
        sys.exit()


def writeJsonStringToFile(jsonString, jsonFile):
   if ok:
      j = json.loads(jsonString)
      with open(jsonFile, 'w') as outfile:
          json.dump(j, outfile, indent=4)


def getDevices():
    URL = "https://api.fitbit.com/1/user/-/devices.json"
    ok, out = makeAPICall(
        URL, AccessToken, RefreshToken)
    return ok, out


def getAlarms():
    ALARMS_URL = "https://api.fitbit.com/1/user/-/devices/tracker/" + deviceId + "/alarms.json"
    ok, out = makeAPICall(
        ALARMS_URL, AccessToken, RefreshToken)
    return ok, out


def getProfile():
    # This is the Fitbit URL to use for the API call
    PROFILE_URL = "https://api.fitbit.com/1/user/-/profile.json"

    ok, out = makeAPICall(
        PROFILE_URL, AccessToken, RefreshToken)
    return ok, out


# This makes an API call.  It also catches errors and tries to deal with them
def makeAPICall(in_url, AccToken, RefToken):
    # Start the request
    req = urllib.request.Request(in_url)

    # Add the access token in the header
    req.add_header('Authorization', 'Bearer ' + AccToken)

# print "I used this access token " + AccToken

    # Fire off the request
    try:
        # Do the request
        response = urllib.request.urlopen(req)

        # Read the response
        full_response = response.read()

        # Return values
        return True, full_response

    # Catch errors, e.g. A 401 error that signifies the need for a new access token
    except urllib.error.URLError as e:
        print("Got this HTTP error: " + str(e.code))
        http_error_message = str(e.read())
        if (e.code == 401) and (http_error_message.find("expired_token") > 0):
            get_new_access_token(RefToken)
            return False, TokenRefreshedOK

        print("This was in the HTTP error message: " + http_error_message)
        writeJsonStringToFile(http_error_message, "error.json")
        # Return that this didn't work, allowing the calling function to handle it
        return False, ErrorInAPI


def create_tokens_file():

    NewAccessToken = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1WDZHQkgiLCJhdWQiOiIyMkQ3SlMiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM4ODg3MzY5LCJpYXQiOjE1Mzg4NTg1Njl9.H-WRCuJvAwX_bgl3NaOYXM35mKkoQBhzF7C1zMtYq_I'
    NewRefreshToken = 'c71772ff8c2e7f1d34cf5bd21474aaaba91b5c359257b1b978428c75560bd06a'
    WriteConfig(NewAccessToken, NewRefreshToken)


# Main part of the code
# Declare these global variables that we'll use for the access and refresh tokens

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

if not ok:
    if (devices == TokenRefreshedOK):
        print("Refreshed the access token.  Can go again")
    else:
        print(ErrorInAPI)
