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
    bucket_origin = args.get('bucket_origin')
    bucket_dest = args.get('bucket_dest')
    environment = args.get('environment')
    advito_application_id = args.get('advito_application_id')
    validation_passed = False
    if job_ingestion_id and bucket_origin:
        validation_passed = Validator().validate(
            job_ingestion_id=job_ingestion_id,
            bucket_origin=bucket_origin,
            bucket_dest=bucket_dest,
            environment=environment,
            advito_application_id=advito_application_id)
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
