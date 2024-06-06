import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.client('s3')




    return {"statusCode": 200,
            "body": json.dumps({"message": "hello world clean_parties"}), }
