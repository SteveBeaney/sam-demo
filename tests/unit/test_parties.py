import json
from datetime import datetime, timedelta
from pprint import pprint
from unittest import TestCase, mock

import boto3

import functions.clean_parties.app as clean
import functions.stage_parties.app as stage
from tests.data.party_data import party_raw
from tests.mocks.mock_requests import mocked_requests_get

_PARTY_STAGE_EVENT = {"url": "https://api.oireachtas.ie/v1/parties?chamber_id=&chamber=dail&house_no=33&limit=5000",
                      "bucket": "sbeaney-sam-staging-test", "dag": "party", "prior_operation": "",
                      "td": "2024-06-07T00:00:00Z", }

_PARTY_CLEAN_EVENT = {"bucket": "sbeaney-sam-staging-test", "dag": "party", "prior_operation": "fetch_stage_data",
                      "td": "2024-06-07T00:00:00Z", "max_keys": 5}
_PARTY_CLEAN_EVENT_NO_MAX = {"bucket": "sbeaney-sam-staging-test", "dag": "party", "prior_operation": "fetch_stage_data",
                      "td": "2024-06-07T00:00:00Z"}

s3 = boto3.client('s3')


class TestLambda(TestCase):

    def setup_method(self, test_method):
        party_obj = json.loads(party_raw)
        start_date = datetime(2024, 1, 1)
        for i in range(6):
            key = '{dag}/{oper}/{td}/{sd}/raw_party.json'.format(dag='party', oper='fetch_stage_data',
                                                                 td='2024-06-07T00:00:00Z',
                                                                 sd=start_date.strftime('%Y-%m-%d %M:%S'))
            s3.put_object(Bucket='sbeaney-sam-staging-test', Key=key, Body=json.dumps({"raw": "none"}))
            start_date += timedelta(seconds=5)
        key = '{dag}/{oper}/{td}/{sd}/raw_party.json'.format(dag='party', oper='fetch_stage_data',
                                                             td='2024-06-07T00:00:00Z',
                                                             sd=start_date.strftime('%Y-%m-%d %M:%S'))
        s3.put_object(Bucket='sbeaney-sam-staging-test', Key=key, Body=json.dumps(party_obj))

    def teardown_method(self, test_method):
        bucket_name = 'sbeaney-sam-staging-test'
        prefix = 'party/fetch_stage_data/'
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in page_iterator:
            if 'Contents' in page:
                objects_to_delete = [{'Key': obj['Key']} for obj in page['Contents']]
                s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete, 'Quiet': True})

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_stage_parties(self, mock_get):
        o = stage.lambda_handler(event=_PARTY_STAGE_EVENT, context={})
        self.assertEqual(o['statusCode'], 200)
        self.assertEqual(o['body']['bucket'], _PARTY_STAGE_EVENT['bucket'])
        raw_data = s3.get_object(Bucket= o['body']['bucket'], Key=o['body']['s3_key'])
        data =(json.loads(raw_data['Body'].read()))
        self.assertEqual('parties' in data['results']['house'], True)


    def test_clean_parties(self):
        o = clean.lambda_handler(event=_PARTY_CLEAN_EVENT, context={})
        self.assertEqual(o['statusCode'], 200)
        self.assertEqual('parties' in o['body'], True)
        o = clean.lambda_handler(event=_PARTY_CLEAN_EVENT_NO_MAX, context={})
        self.assertEqual(o['statusCode'], 200)
