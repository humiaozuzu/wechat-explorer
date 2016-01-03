# -*- coding: utf-8 -*-

import os
import sqlite3
import re
import xmltodict
import calendar
import biplist
from datetime import datetime

from we.utils import logger
from we.utils import id_to_digest


class RecordType:
    SYSTEM = 10000
    SHORT_VIDEO = 62
    CALL = 50
    LINK = 49
    LOCATIOM = 48
    EMOTION = 47
    VIDEO = 43
    CARD = 42
    VOICE = 34
    IMAGE = 3
    TEXT = 1

RecordTypeCN = {
    RecordType.SYSTEM: u'系统消息',
    RecordType.SHORT_VIDEO: u'小视频',
    RecordType.CALL: u'语音电话/视频电话',
    RecordType.LINK: u'链接/红包',
    RecordType.LOCATIOM: u'位置',
    RecordType.EMOTION: u'动画表情',
    RecordType.VIDEO: u'视频',
    RecordType.CARD: u'名片',
    RecordType.VOICE: u'语音',
    RecordType.IMAGE: u'图片',
    RecordType.TEXT: u'文本',
}

FriendTypeExlude = (
    0,
    1,
    2, # groups etc
    4, # friends only in group chat
    6, # friends only in group chat
    64, # 语音提醒
)


class WechatParser(object):

    def __init__(self, path, user_id):
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):
            raise IOError('Path `%s` not exist for user %s' % (self.path, user_id))
        self.user_id = user_id
        self.user_hash = id_to_digest(user_id)

    def get_labels(self):
        plist_path = self.path + '/%s/contactlabel.list' % self.user_hash
        pl = biplist.readPlist(plist_path)
        obj_idxs = pl['$objects'][1]['NS.objects']

        label_map = {}
        for idx in obj_idxs:
            idx = int(idx)
            label_map[pl['$objects'][idx]['m_uiID']] = pl['$objects'][idx+1]

        return label_map

    def get_friends(self):
        chat_db = self.path + '/%s/DB/MM.sqlite' % self.user_hash
        logger.debug('DB path %s' % chat_db)
        conn = sqlite3.connect(chat_db)

        friends = []
        for row in conn.execute('SELECT f.*,fe.ConStrRes2, fe.ConRemark FROM Friend as f JOIN Friend_Ext as fe USING(UsrName) WHERE `Type` NOT IN %s AND `UsrName` NOT LIKE "gh_%%"' % FriendTypeExlude.__str__()):
            label_pattern = '<LabelList>(.*)</LabelList>'
            label_list_str = re.search(label_pattern, row[13], re.MULTILINE).group(1)
            label_list = label_list_str.split(',')
            label_list = [int(label_id) for label_id in label_list if label_id]

            friend = dict(
                id=row[1],
                nickname=row[2],
                gender=row[6],
                type=row[10],
                label_ids = label_list,
                remark = row[14],
            )
            friends.append(friend)
        return friends

    def get_chatrooms(self):
        chat_db = self.path + '/%s/DB/MM.sqlite' % self.user_hash
        logger.debug('DB path %s' % chat_db)
        conn = sqlite3.connect(chat_db)

        friends = []
        for row in conn.execute('SELECT * FROM `Friend` WHERE `UsrName` LIKE "%chatroom"'):
            friend = dict(
                id=row[1],
                nickname=row[2],
                type=row[10],
            )
            friends.append(friend)
        return friends

    def get_chatroom_friends(self, chatroom_id):
        session_db = self.path + '/%s/session/session.db' % self.user_hash
        logger.debug('DB path %s' % session_db)
        group_table = 'SessionAbstract'
        conn = sqlite3.connect(session_db)

        # GET group users nickname xml file
        c = conn.execute('SELECT * FROM %s WHERE UsrName="%s"' % (group_table, chatroom_id))
        row = c.fetchone()
        session_path = row[5]
        full_session_path = self.path + '/%s%s' % (self.user_hash, session_path)
        logger.debug('Bin path %s' % full_session_path)

        f = open(full_session_path, 'r')
        raw_xml = f.read()
        pattern = '<RoomData>.*</RoomData>'
        chatroom_xml = re.search(pattern, raw_xml, re.MULTILINE).group()
        xml_dict = xmltodict.parse(chatroom_xml)

        friends = []
        for member in xml_dict['RoomData']['Member']:
            friend = dict(
                id=member['@UserName'],
                nickname=member.get('DisplayName'),
            )
            friends.append(friend)
        return friends

    def get_friend_records(self):
        pass

    def get_chatroom_records(self, chatroom_id, start=datetime(2000, 1, 1), end=datetime(2050, 1, 1)):
        chatroom_hash = id_to_digest(chatroom_id)
        chatroom_table = 'Chat_' + chatroom_hash

        start = calendar.timegm(start.utctimetuple())
        end = calendar.timegm(end.utctimetuple())

        chat_db = self.path + '/%s/DB/MM.sqlite' % self.user_hash
        logger.debug('DB path %s' % chat_db)
        conn = sqlite3.connect(chat_db)

        records = []
        for row in conn.execute("SELECT * FROM %s WHERE CreateTime BETWEEN '%s' and '%s'" % (chatroom_table, start, end)):
            created_at, msg, msg_type, not_self = row[3], row[4] ,row[7], row[8]
            user_id = None

            # split out user_id in msg
            id_contained_types = (RecordType.TEXT, RecordType.IMAGE, RecordType.VOICE,
                                  RecordType.CARD, RecordType.EMOTION, RecordType.LOCATIOM,
                                  RecordType.LINK)
            if not_self and msg_type in id_contained_types:
                user_id, msg = row[4].split(':\n', 1)

            # TODO: get user_id in non id_contained_types

            if not not_self:
                user_id = self.user_id

            record = dict(
                user_id=user_id,
                msg=msg,
                type=msg_type,
                not_self=not_self,
                created_at=created_at
            )
            records.append(record)
        return records
