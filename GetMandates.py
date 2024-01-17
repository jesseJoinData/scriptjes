import requests
import json
import csv
import os
import sys
import pandas as pd

kvkUitvragendePartij = "12035790"

def getAccessToken():
    clientID = 'purpose-registry-client'
    clientSecret = '8eefee19-b193-4cc9-bf45-7f6e2b0aa8b6'
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

def getMandates(ownerKvK):
    accessToken = getAccessToken()

    url = f'https://production.join-data.net/api/purpose-registry/v1/companies/nl.kvk/{ownerKvK}/participations/providing-companies/nl.kvk/{kvkUitvragendePartij}'

    headers = {'Authorization': f'Bearer {accessToken}'}

    companyMappingResponse = requests.get(url, headers=headers)
    
    if companyMappingResponse.status_code != 200:
        print("companyMapping request returns:", companyMappingResponse.status_code)
        return companyMappingResponse
    else:
        return companyMappingResponse

sourceFolder = 'input'
destinationFolder = 'json_files'
files = os.listdir(sourceFolder)
if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)

failedFolder = 'failed'
if not os.path.exists(failedFolder):
    os.mkdir(failedFolder)

failedFile = os.path.join(failedFolder, 'failedGetMapping.csv')

for index, filename in enumerate(files):
    inputFile = sourceFolder + '\\' + filename
    df = pd.read_csv(inputFile, delimiter=';')

    for row_index, row in df.iterrows():
        if pd.isna(df.at[row_index, 'TargetCompanyKvk']):

            if not os.path.exists(failedFile):
                failFile = pd.DataFrame(columns=['rowFailed'])
                failFile.to_csv(failedFile, sep=';', index=False)
            
            data = {'rowFailed': [row_index + 2]}
            appendData = pd.DataFrame(data)

            appendData.to_csv(failedFile, sep=';', mode='a', index=False, header=False)
        else:
            ownerKvk = str(row['TargetCompanyKvk']).zfill(8)
            companyMappingJson = getMandates(ownerKvk)

            if companyMappingJson.status_code == 200:
                output_file_path = os.path.join(destinationFolder, f"Mandate{ownerKvk}.json")
                output_file = open(output_file_path, 'wb')
                output_file.write(companyMappingJson.content)
            else:
                print("something went wrong with:", ownerKvk)

if not os.path.exists(failedFile):
    failFile = pd.DataFrame(columns=['rowFailed'])
    failFile.to_csv(failedFile, sep=';', index=False)

data = {'rowFailed': ['', '']}
appendData = pd.DataFrame(data)
appendData.to_csv(failedFile, sep=';', mode='a', index=False, header=False)