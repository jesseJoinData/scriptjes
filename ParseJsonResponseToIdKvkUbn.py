import json
import pandas as pd
import os

sourceFolder = 'json_filesPart'
destinationFolder = 'withUbnRestriction'

if not os.path.exists(sourceFolder):
    print(f"The source folder path '{sourceFolder}' does not exist.")
else:
    if not os.path.exists(destinationFolder):
        os.mkdir(destinationFolder)
    withRestrictionFile = destinationFolder + '\\' + 'withUbnRestriction.csv'
    if not os.path.exists(withRestrictionFile):
        failFile = pd.DataFrame(columns=['id', 'Kvk', 'ubn'])
        failFile.to_csv(withRestrictionFile, sep=',', index=False)

    files = os.listdir(sourceFolder)

    for index, filename in enumerate(files):
        inputFile = sourceFolder + '\\' + filename
        # outputFile = destinationFolder + '\\' + os.path.splitext(filename)[0] + 'IDs.csv'
        jsonFile = open(inputFile, 'r')
        data = json.load(jsonFile)

        first_ids = []
        Kvklist = []
        ubnlist = []

        # Loop through the data blocks
        for block in data['data']:
            for restriction in block.get('restrictions', []):
                if restriction.get('description') == "Data restrictie op locatie" and restriction.get('scheme') == "nl.ubn":
                    first_ids.append(block['id'])
                    Kvklist.append(block['companyValue'])
                    ubnlist.append(restriction.get('value'))
                    break  # Stop processing restrictions for this block once we've found the first "id"

        # Print the first "id" values for blocks with the specified description
        for id, Kvk, ubn in zip(first_ids, Kvklist, ubnlist):
            data = {'id': [id],
                    'Kvk': [Kvk],
                    'ubn': [ubn]
                    }
            appendData = pd.DataFrame(data)

            appendData.to_csv(withRestrictionFile, sep=',', mode='a', index=False, header=False)
            