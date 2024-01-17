import requests
import json
import csv
import os
import sys
import pandas as pd

def getAccessToken():
    clientID = '9c909f64'
    clientSecret = 'sRm9SS0LEIxvB5Movg7KgMOIyNdPXlVy' #credentials for ABAB

    # clientID = 'c860108b'
    # clientSecret = 'cdba89ab-8af5-4442-a210-7cc949ef844b' #credentials for countus

    data = {'grant_type': 'client_credentials'}

    url = f'https://production.join-data.net/auth/realms/datahub/protocol/openid-connect/token'

    accessTokenResponse = requests.post(url, data = data, auth = (clientID, clientSecret))
    
    if accessTokenResponse.status_code == 200:
        
        data = accessTokenResponse.json()
        accessToken = data.get('access_token', '')
    else:
        print("accessToken request returns:", accessTokenResponse.status_code)
        sys.exit()
    
    return accessToken

def getParticipations(ID):
    accessToken = getAccessToken()

    purposeID = ID
    url = f'https://production.join-data.net/purpose-registry/api/v1.0/purposes/{purposeID}/participations'

    headers = {'Authorization': f'Bearer {accessToken}'}

    participationResponse = requests.get(url, headers=headers)
    
    if participationResponse.status_code != 200:
        print("getParticipation request returns:", participationResponse.status_code)
        return participationResponse
    else:
        return participationResponse
    
sourceFolder = 'inputPart'
destinationFolder = 'json_filesPart'
files = os.listdir(sourceFolder)
if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)

for index, filename in enumerate(files):
    inputFile = sourceFolder + '\\' + filename
    df = pd.read_csv(inputFile)

    for row_index, row in df.iterrows():
        if pd.isna(df.at[row_index, 'purpose_id']):
            print("failed")
        else:
            purposeID = str(row['purpose_id'])
            participationJson = getParticipations(purposeID)
            print(participationJson.status_code)

            if participationJson.status_code == 200:
                output_file_path = os.path.join(destinationFolder, f"{purposeID}.json")
                output_file = open(output_file_path, 'wb')
                output_file.write(participationJson.content)
            else:
                print("something went wrong with:", purposeID)
