import falcon
import json
import msgpack
from logging import getLogger,DEBUG,StreamHandler
from app.main import compare_two_text

logger = getLogger(__name__)
sh = StreamHandler()
sh.setLevel(DEBUG)
logger.addHandler(sh)
logger.setLevel(DEBUG)


class Compare(object):
    def on_get(self,req,resp):
        params = req.params
        logger.debug(params)
        if('word1' in params and 'word2' in params):
            try:
                result = compare_two_text(params['word1'],params['word2'])
                resp.data = msgpack.packb(result,use_bin_type=False)
                resp.content_type = falcon.MEDIA_MSGPACK
                resp.status = falcon.HTTP_200
                logger.debug(result)
                return
            except:
                import traceback
                logger.error(traceback.print_exc())
                resp.status = falcon.HTTP_502
                return

        # パラメータ不整合はユーザーエラー
        resp.status = falcon.HTTP_400
        return

api = application = falcon.API()
compare = Compare()
api.add_route('/compare',compare)