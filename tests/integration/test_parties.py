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
                      "td": "1962-08-07T08:30:00Z", }

_PARTY_CLEAN_EVENT = {"bucket": "sbeaney-sam-staging-test", "dag": "party", "prior_operation": "fetch_stage_data",
                      "td": "1962-08-07T08:30:00Z"}

s3 = boto3.client('s3')


class TestLambda(TestCase):


    def teardown_method(self, test_method):
        bucket_name = 'sbeaney-sam-staging-test'
        prefix = 'party/fetch_stage_data/962-08-07T08:30:00Z/'
        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in page_iterator:
            if 'Contents' in page:
                objects_to_delete = [{'Key': obj['Key']} for obj in page['Contents']]
                s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete, 'Quiet': True})

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_parties(self, mock_get):
        o = stage.lambda_handler(event=_PARTY_STAGE_EVENT, context={})
        self.assertEqual(o['statusCode'], 200)
        o = clean.lambda_handler(event=_PARTY_CLEAN_EVENT, context={})
        self.assertEqual(o['statusCode'], 200)

