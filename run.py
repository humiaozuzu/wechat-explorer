# -*- coding: utf-8 -*-

import argparse
import datetime

from we.wechat import WechatParser
from we.wechat import RecordTypeCN
from we.contrib.chatroom_analytics import ChatroomAnalytics

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

args = parser.parse_args()

if args.command == 'list_friends':
    wechat = WechatParser(args.path, args.user_id)
    friends = wechat.get_friends()
    for friend in friends:
        msg = '%s %s' % (friend['id'], friend['nickname'])
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

    ca = ChatroomAnalytics(args.path, args.user_id, args.chatroom_id, args.start_at, args.end_at)
    stats = ca.get_stats(friends)

    counters = stats['counters']
    for k, v in counters.items():
        print '%s: %s' % (RecordTypeCN[k], v)

    users_count = stats['users_rank']
    print '\nTop 50 least talking:'
    for i, user in enumerate(users_count[:50], 1):
        print '%d %s: %s' % (i, id_nicknames[user[0]] or u'已退群', user[1])

    print '\nTop 50 most talking:'
    for i, user in enumerate(reversed(users_count[-50:]), 1):
        print '%d %s: %s' % (i, id_nicknames[user[0]] or u'已退群', user[1])

    silent_users = stats['silent_users']
    print '\nSlient users:'
    for user_id in silent_users:
        print '%s %s' % (user_id, id_nicknames[user_id] or u'已退群')


elif args.command == 'get_chatroom_user_stats':
    stats = ChatroomAnalytics(args.path, args.user_id, args.chatroom_id, args.start_at, args.end_at)
    print stats.get_user_stats(args.chatroom_user_id)
