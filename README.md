# Wechat Explorer

> 微信聊天记录导出、分析工具 For iOS

## Guide

``` bash
python run.py list_chatrooms ../Documents user_id
python run.py list_friends ../Documents user_id
python run.py get_chatroom_stats ../Documents user_id chatroom_id@chatroom 2015-08-01 2015-09-01
python run.py export_chatroom_records ../Documents user_id chatroom_id@chatroom 2015-10-01 2015-10-07 ../
```

HTML chatroom records to PDF

``` bash
wkhtmltopdf --dpi 300 records.html records.pdf
```

## TODO

- support non-text record type
