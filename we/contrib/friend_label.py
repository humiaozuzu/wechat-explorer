# -*- coding: utf-8 -*-

from we.wechat import WechatParser


class FriendLabel(object):

    def __init__(self, path, user_id):
        self.wechat = WechatParser(path, user_id)

    def get_stats(self):
        friends = self.wechat.get_friends()

        non_label_users = []
        multi_label_users = []
        # list friends without labels and with more than one label
        for user in friends:
            label_count = len(user['label_ids'])
            if label_count == 0:
                non_label_users.append(user)
            elif label_count > 1:
                multi_label_users.append(user)
        return dict(non_label_users=non_label_users, multi_label_users=multi_label_users)
