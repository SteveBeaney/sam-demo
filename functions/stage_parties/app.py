import json
import logging
from datetime import datetime, timezone

import boto3
import requests

logger = logging.getLogger()
logger.setLevel("INFO")

_OPERATION = "fetch_stage_data"


def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    url = event["url"]
    bucket = event["bucket"]
    dag = event["dag"]
    td = event["td"]
    sd = datetime.now(tz=timezone.utc).isoformat()
    key = '{dag}/{oper}/{td}/{sd}/raw_party.json'.format(dag=dag,
                                                         oper=_OPERATION,
                                                         td=td, sd=sd)
    response = requests.get(url)

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(response.json()))

    return {"statusCode": 200,
            "body": {"bucket": bucket, "dag": dag, "operation": _OPERATION,
                     "td": td, "sd": sd, "s3_key": key}}
