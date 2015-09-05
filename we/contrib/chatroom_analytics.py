# -*- coding: utf-8 -*-

import operator

from we.wechat import WechatParser
from we.wechat import RecordType


class ChatroomAnalytics(object):

    def __init__(self, path, user_id, chatroom_id, start_at, end_at):
        self.wechat = WechatParser(path, user_id)
        self.records = self.wechat.get_chatroom_records(chatroom_id, start_at, end_at)

    def get_stats(self, members=None):
        # build stats for counters
        counters = {
            RecordType.SHORT_VIDEO: 0,
            RecordType.LINK: 0,
            RecordType.LOCATIOM: 0,
            RecordType.EMOTION: 0,
            RecordType.VIDEO: 0,
            RecordType.CARD: 0,
            RecordType.VOICE: 0,
            RecordType.IMAGE: 0,
            RecordType.TEXT: 0,
        }

        for record in self.records:
            try:
                counters[record['type']] += 1
            except KeyError:
                continue

        # build stats for ranks
        users_count = {}
        for record in self.records:
            if not record['user_id']:
                continue
            users_count[record['user_id']] = users_count.get(record['user_id'], 0) + 1
        users_rank = sorted(users_count.items(), key=operator.itemgetter(1))

        # build stats for silent users
        member_ids = [member['id'] for member in members]
        actice_users = users_count.keys()
        silent_users = []
        for user_id in member_ids:
            if user_id not in actice_users:
                silent_users.append(user_id)

        return dict(counters=counters,
                    users_rank=users_rank,
                    silent_users=silent_users)

    def get_user_stats(self, user_id):
        pass
