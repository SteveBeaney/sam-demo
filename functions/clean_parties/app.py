import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel("INFO")

_OPERATION = "clean_stage_data"


def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    bucket = event["bucket"]
    dag = event["dag"]
    prior_operation = event["prior_operation"]
    td = event["td"]
    if "max_keys" in event:
        max_keys = event["max_keys"]
    else:
        max_keys = 1000

    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket,
              'Prefix': '{dag}/{oper}/{td}/'.format(dag=dag,
                                                    oper=prior_operation,
                                                    td=td),
              'MaxKeys': max_keys, }
    keys = []
    while True:
        response = s3.list_objects_v2(**kwargs)
        if 'Contents' in response:
            for obj in response['Contents']:
                if 'raw_party.json' in obj['Key']:
                    keys.append(obj['Key'])
        if response.get('IsTruncated'):  # If truncated, there are more keys
            kwargs['ContinuationToken'] = response['NextContinuationToken']
        else:
            break
    raw_key = sorted(keys, reverse=True)[0]

    raw_data = s3.get_object(Bucket=bucket, Key=raw_key)
    body = json.loads(raw_data['Body'].read())
    parties = [party['party']['showAs'] for party in
               body['results']['house']['parties']]
    return {"statusCode": 200, "body": json.dumps({"parties": parties})}
