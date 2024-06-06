import json
import logging

import boto3
import requests
import uuid as _uuid

logger = logging.getLogger()
logger.setLevel("INFO")

_OPERATION = "fetch_stage_data"

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    url = event["url"]
    bucket = event["bucket"]
    dag = event["dag"]
    uuid = _uuid.uuid4()
    key = '{dag}/{oper}/{uuid}'.format(dag=dag,oper=_OPERATION,uuid=uuid)
    response = requests.get(url)

    s3 = boto3.client('s3')

    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(response.json()))

    return {"statusCode": 200,
            "body": {"bucket": bucket,
                     "uuid": str(uuid),
                     "operation": _OPERATION,
                     "s3_key":key
                     }
            }


