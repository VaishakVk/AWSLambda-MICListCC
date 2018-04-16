import pandas as pd
import json
import numpy as np
import requests
import boto3


def lambda_handler(event, context):
    try:
        excelURL = 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls'
        imageRequest = requests.get(excelURL)  # create HTTP response object
        fileName = 'ISO10383_MIC_Test.xls'  # File Name to be saved as

        with open('/tmp/' + fileName, 'wb') as f:
            f.write(imageRequest.content)

        # Read 'MICs List by CC' sheet using Pandas library and create Dataframe
        # Store in /tmp folder
        fileLoad = pd.ExcelFile('/tmp/' + fileName)
        dfMIClistCC = fileLoad.parse('MICs List by CC')

        # Replace Nan from Dataframe and convert to empty string
        dfMIClistCC = dfMIClistCC.replace(np.nan, '')

        # Convert Panda Dataframe to Dictionary
        dfMIClistCC_dict = dfMIClistCC.to_dict('records')

        # Convert Dictionary to JSON
        dfMIClistCC_str = json.dumps(dfMIClistCC_dict)
        dfMIClistCC_json = json.loads(dfMIClistCC_str)

        # Save JSON file
        # Store in /tmp folder
        with open('/tmp/dfMIClistCC.json', 'w') as f:
            json.dump(dfMIClistCC_json, f)

        # Upload JSON file to S3 bucket
        data = open('/tmp/dfMIClistCC.json', 'rb')
        s3 = boto3.client('s3')
        s3.put_object(Bucket='bucket-miclistcc',
                      Key='MICListCC.json',
                      Body=data)
        return 'File uploaded successfully'
    except ConnectionError:
        print('Content does not exist')
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print('Error occured: ' + str(e))
