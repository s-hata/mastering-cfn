import json
import logging
import signal
import urllib.request

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    signal.alarm((context.get_remaining_time_in_millis() // 1000) - 1)
    try:
        LOGGER.info(f"REQUEST RECEIVED[event]:\n ${event}")
        LOGGER.info(f"REQUEST RECEIVED[context]:\n ${context}")
        if event["RequestType"] == "Create":
            create_handler(event, context)
        elif event["RequestType"] == "Update":
            update_handler(event, context)
        elif event["RequestType"] == "Delete":
            delete_handler(event, context)
        else:
            LOGGER.info("FAILED!")
            send_response(event, context, "FAILED",
                          {"Message": "Unexpected event received from CloudFormation"})
    except:
        LOGGER.info("FAILED!")
        send_response(event, context, "FAILED", {"Message": "Exception during processing"})
    finally:
        signal.alarm(0)


def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": response_data
    }).encode("utf-8")

    LOGGER.info(f"ResponseURL: {event['ResponseURL']}")
    LOGGER.info(f"ResponseBody: {response_body}")

    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    request = urllib.request.Request(event["ResponseURL"], data=response_body)
    request.add_header("Content-Type", "")
    request.add_header("Content-Length", len(response_body))
    request.get_method = lambda: "PUT"
    response = opener.open(request)
    LOGGER.info(f"Status code: {response.getcode()}")
    LOGGER.info(f"Status message: {response.msg}")


def create_handler(event, context):
    LOGGER.info("CREATE!")
    send_response(event, context, "SUCCESS",
                  {"Message": "Resource creation successful!"})


def update_handler(event, context):
    LOGGER.info("UPDATE!")
    send_response(event, context, "SUCCESS",
                  {"Message": "Resource update successful!"})


def delete_handler(event, context):
    LOGGER.info("DELETE!")
    send_response(event, context, "SUCCESS",
                  {"Message": "Resource deletion successful!"})


def timeout_handler(_signal, _frame):
    raise Exception("Time exceeded")


signal.signal(signal.SIGALRM, timeout_handler)
