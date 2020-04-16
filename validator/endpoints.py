# coding=UTF-8
import json


def validation(event, context):
    """
    /api/{controller}/{method}/{c}/{d}
    /api/{controller}/{method}/{c}
    :param event:
    :param context:
    :return:
    """
    from validator import Validator
    args = event.get('body')
    args = json.loads(args) if type(args) != dict else args
    job_ingestion_id = args.get('job_ingestion_id')
    bucket_name = args.get('bucket_name')
    validation_passed = False
    if job_ingestion_id and bucket_name:
        validation_passed = Validator().validate(
            job_ingestion_id=job_ingestion_id,
            bucket_name=bucket_name)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Methods': "*",
            'Access-Control-Allow-Headers': "*",
        },
        'body': json.dumps(
            {
                'success': validation_passed,
            })
    }
