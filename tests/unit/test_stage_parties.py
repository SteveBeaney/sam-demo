import json
from unittest import TestCase
import boto3

import functions.clean_parties.app as clean
import functions.stage_parties.app as stage

_PARTY_STAGE_EVENT = {"url": "https://api.oireachtas.ie/v1/parties?chamber_id=&chamber=dail&house_no=33&limit=5000",
                "bucket":"sbeaney-sam-staging",
                "dag": "party"
                }
_UUID = 'a608807e-fab9-4563-8d86-51933b5c05c1'
_PARTY_DATA

class TestLambda(TestCase):
    def test_clean_parties(self):
        o = clean.lambda_handler(event={}, context={})
        s3 = boto3.client('s3')
        s3_key = f'{_PARTY_STAGE_EVENT["dag"]}/fetch_stage_data/{_UUID}'
        response = s3.get_object(Bucket=_PARTY_STAGE_EVENT['bucket'], Key=s3_key)
        data = response['Body'].read().decode('utf-8')
        print(data)
        self.assertEqual(o['statusCode'], 200)  # add assertion here
        self.assertEqual(o['body'], '{"message": "hello world clean_parties"}')  # add assertion here


    def test_stage_parties(self):
        o = stage.lambda_handler(event=_PARTY_STAGE_EVENT, context={})
        self.assertEqual(o['statusCode'], 200)  # add assertion here
        self.assertEqual(o['body']['bucket'], _PARTY_STAGE_EVENT['bucket'])

