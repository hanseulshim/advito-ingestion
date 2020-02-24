# coding=UTF-8
import json


def api_get(event, context):
    """
    /api/{controller}/{method}/{c}/{d}
    /api/{controller}/{method}/{c}
    :param event:
    :param context:
    :return:
    """
    from validator import Validator
    res, msg = Validator.validate(
        ingest_job_id='123456789',
        file_path='https://hotel-api-downloads.s3.us-east-2.amazonaws.com/ValidationTest.xlsx')

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
                'success': res,
                'message': msg
            })
    }


if __name__ == '__main__':
    print(api_get({}, {}))
