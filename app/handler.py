from logging import getLogger,DEBUG,StreamHandler
from app.compare_service import compare_two_text
import msgpack
import base64
import json

logger = getLogger(__name__)
sh = StreamHandler()
sh.setLevel(DEBUG)
logger.addHandler(sh)
logger.setLevel(DEBUG)

def lambda_handler(event,context):
    logger.debug(event)
    try:
        request_body = json.loads(event['body'])
        all_result = []
        for comparison in request_body['comparisons']:
            result = compare_two_text(request_body['target'],comparison)
            all_result.append(result)
        return {
            'statusCode':200,
            'body':base64.b64encode(msgpack.packb(all_result,use_bin_type=False)).decode('utf-8'),
            'headers':{
                'Content-Type':'application/x-msgpack'
            },
            'isBase64Encoded':True

        }
    except json.JSONDecodeError as e:
        logger.error(e)
        return {
            'statusCode':400,
            'body':'json decode error',
            'headers':{
                'Content-Type':'application/json'
            }
        }
    except KeyError as e:
        logger.error(e)
        return {
            'statusCode':400,
            'body':'parameter error',
            'headers':{
                'Content-Type':'application/json'
            }
        }
    except Exception as e:
        logger.error(e)
        return {
            'statusCode':502,
            'body':'unexpected error',
            'headers':{
                'Content-Type':'application/json'
            }
        }
