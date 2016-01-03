# -*- coding: utf-8 -*-

import argparse
import datetime
import logging

from we.wechat import WechatParser
from we.wechat import RecordTypeCN

def main():
    logger = logging.getLogger('wechat_parser')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel('DEBUG')

    parser = argparse.ArgumentParser(prog='Wechat Explorer')
    subparser = parser.add_subparsers(dest='command', help='sub-command help')

    p1 = subparser.add_parser('list_friends', help='list all friends')
    p1.add_argument('path', type=str)
    p1.add_argument('user_id', type=str)
    p2 = subparser.add_parser('list_chatrooms', help='list all chatrooms')
    p2.add_argument('path', type=str)
    p2.add_argument('user_id', type=str)
    p3 = subparser.add_parser('get_chatroom_stats', help='get chatroom stats')
    p3.add_argument('path', type=str)
    p3.add_argument('user_id', type=str)
    p3.add_argument('chatroom_id', type=str)
    p3.add_argument('start_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p3.add_argument('end_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p4 = subparser.add_parser('get_chatroom_user_stats', help='get chatroom user stats')
    p4.add_argument('path', type=str)
    p4.add_argument('user_id', type=str)
    p4.add_argument('chatroom_id', type=str)
    p4.add_argument('chatroom_user_id', type=str)
    p4.add_argument('start_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p4.add_argument('end_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p5 = subparser.add_parser('export_chatroom_records', help='export chatroom records as HTML')
    p5.add_argument('path', type=str)
    p5.add_argument('user_id', type=str)
    p5.add_argument('chatroom_id', type=str)
    p5.add_argument('start_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p5.add_argument('end_at', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    p5.add_argument('export_path', type=str)
    p6 = subparser.add_parser('get_friend_label_stats', help='get friend label stats')
    p6.add_argument('path', type=str)
    p6.add_argument('user_id', type=str)

    args = parser.parse_args()

    if args.command == 'list_friends':
        wechat = WechatParser(args.path, args.user_id)
        friends = wechat.get_friends()
        for friend in friends:
            msg = '%s %s(%s)' % (friend['id'], friend['nickname'], friend['remark'])
            print msg.encode('utf-8')
    elif args.command == 'list_chatrooms':
        wechat = WechatParser(args.path, args.user_id)
        friends = wechat.get_chatrooms()
        for friend in friends:
            msg = '%s %s' % (friend['id'], friend['nickname'])
            print msg.encode('utf-8')
    elif args.command == 'get_chatroom_stats':
        wechat = WechatParser(args.path, args.user_id)
        friends = wechat.get_chatroom_friends(args.chatroom_id)
        id_nicknames = {friend['id']: friend['nickname'] for friend in friends}

        from we.contrib.chatroom_analytics import ChatroomAnalytics
        ca = ChatroomAnalytics(args.path, args.user_id, args.chatroom_id, args.start_at, args.end_at)
        stats = ca.get_stats(friends)

        counters = stats['counters']
        for k, v in counters.items():
            print '%s: %s' % (RecordTypeCN[k], v)

        users_count = stats['users_rank']
        print '\nTop 50 least talking:'
        for i, user in enumerate(users_count[:50], 1):
            print '%d %s: %s' % (i, id_nicknames.get(user[0]) or u'已退群', user[1])

        print '\nTop 50 most talking:'
        for i, user in enumerate(reversed(users_count[-50:]), 1):
            print '%d %s: %s' % (i, id_nicknames.get(user[0]) or u'已退群', user[1])

        silent_users = stats['silent_users']
        print '\nSlient users:'
        for user_id in silent_users:
            print '%s %s' % (user_id, id_nicknames.get(user_id) or u'已退群')
    elif args.command == 'get_chatroom_user_stats':
        from we.contrib.chatroom_analytics import ChatroomAnalytics
        stats = ChatroomAnalytics(args.path, args.user_id, args.chatroom_id, args.start_at, args.end_at)
        print stats.get_user_stats(args.chatroom_user_id)
    elif args.command == 'export_chatroom_records':
        from we.contrib.html_exporter import HTMLExporter
        exporter = HTMLExporter(args.path, args.user_id, args.chatroom_id, args.start_at, args.end_at)
        exporter.export(args.export_path)
    elif args.command == 'get_friend_label_stats':
        wechat = WechatParser(args.path, args.user_id)
        labels = wechat.get_labels()

        from we.contrib.friend_label import FriendLabel
        fl = FriendLabel(args.path, args.user_id)
        stats = fl.get_stats()

        print '\nUsers without labels:'
        for user in stats['non_label_users']:
            print '%s %s(%s)' % (user['id'], user['nickname'], user['remark'])
        print '\nUsers with more than 2 labels:'
        for user in stats['multi_label_users']:
            label_str = ','.join([labels[label_id] for label_id in user['label_ids']])
            print '%s %s(%s): %s' % (user['id'], user['nickname'], user['remark'], label_str)

if __name__ == '__main__':
    main()
