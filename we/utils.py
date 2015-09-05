# -*- coding: utf-8 -*-

import logging
import hashlib


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger('wechat_parser')
logger.addHandler(NullHandler())


def id_to_digest(user_id):
    m = hashlib.md5()
    m.update(user_id)
    return m.hexdigest()
