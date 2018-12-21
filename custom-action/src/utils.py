import boto3
import json
import logging


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
client = boto3.client("codepipeline")

def get_params(job_data):
    try:
        params = job_data['actionConfiguration']['configuration']['UserParameters']
        decoded_params = json.loads(params)
    except Exception as e:
        raise Exception('UserParameters could not be decoded as JSON')
    
    if 'stack' not in decoded_params:
        raise Exception('Your UserParameters JSON must include the stack name')
    
    if 'artifact' not in decoded_params:
        raise Exception('Your UserParameters JSON must include the artifact name')
    
    if 'file' not in decoded_params:
        raise Exception('Your UserParameters JSON must include the template file name')
    
    return decoded_params


def fail(job_id, event, context, message):
    response = client.put_job_failure_result(
      jobId=job_id,
      failureDetails={'message': message, 'type': 'JobFailed'}
    )
    LOGGER.info(f"RESPONSE :\n {vars(response)}")


def success(job_id, event, context, message):
    response = client.put_job_success_result(jobId=job_id)
    LOGGER.info(f"RESPONSE :\n {vars(response)}")
