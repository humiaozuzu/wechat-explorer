# -*- coding: utf-8 -*-

import os
import shutil

from jinja2 import Environment, FileSystemLoader

from we.wechat import WechatParser


class HTMLExporter(object):

    def __init__(self, path, user_id, chatroom_id, start_at, end_at):
        self.wechat = WechatParser(path, user_id)
        self.records = self.wechat.get_chatroom_records(chatroom_id, start_at, end_at)
        self.friends = self.wechat.get_chatroom_friends(chatroom_id)

    def export(self, export_path):
        id_nicknames = {friend['id']: friend['nickname'] for friend in self.friends}
        for record in self.records:
            if not record['user_id']:
                continue

            record['nickname'] = id_nicknames.get(record['user_id']) or u'已退群'

        env = Environment(loader=FileSystemLoader('we/contrib/html_exporter_res/'))
        template = env.get_template('wechat.html')
        output_from_parsed_template = template.render(records=self.records)

        # make dir
        export_full_path = os.path.realpath(export_path) + '/records'
        os.makedirs(export_full_path)

        # copy res
        shutil.copytree('we/contrib/html_exporter_res/css', export_full_path+'/css')
        shutil.copytree('we/contrib/html_exporter_res/img', export_full_path+'/img')

        # build records html
        with open(export_full_path+"/records.html", "w") as fh:
            fh.write(output_from_parsed_template.encode('utf8'))
