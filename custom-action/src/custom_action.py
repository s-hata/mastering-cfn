import boto3
from datetime import datetime
import logging
import json
from utils import get_params, fail, success


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
    try:
        LOGGER.info(f"REQUEST RECEIVED[event]:\n {event}")
        LOGGER.info(f"REQUEST RECEIVED[context]:\n {vars(context)}")
        LOGGER.info(f"{event['CodePipeline.job']}");

        job_id = event["CodePipeline.job"]["id"]
        job_data = event["CodePipeline.job"]["data"]
        artifacts = job_data["inputArtifacts"]
        params = get_params(job_data)
        success(job_id, event, context, "Success")

    except:
        LOGGER.info("FAILED!")
        import traceback
        traceback.print_exc()
        fail(job_id, event, context, "Exception during processing")
