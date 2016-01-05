# Wechat Explorer

> 微信聊天记录导出、分析工具 For iOS

## Guide

### Install via pip

``` bash
pip install wechat-explorer
```

### Export wechat data from your iOS backup

You may use the free [iPhone Backup Extractor](http://supercrazyawesome.com/) or iExplorer. Export the folder named `com.tencent.xin`. There is an folder named `Documents` in your exports.

### How to use

``` bash
wexp list_chatrooms ../Documents user_id
wexp list_friends ../Documents user_id
wexp get_chatroom_stats ../Documents user_id chatroom_id@chatroom 2015-08-01 2015-09-01
wexp export_chatroom_records ../Documents user_id chatroom_id@chatroom 2015-10-01 2015-10-07 ../
wexp get_friend_label_stats ../Documents user_id
```

HTML chatroom records to PDF

``` bash
wkhtmltopdf --dpi 300 records.html records.pdf
```

![Demo](https://cloud.githubusercontent.com/assets/300016/12079004/09f2013c-b264-11e5-8a3b-8c6126dc61ae.png)


## 原理

由于 iOS 本身的限制，是拿不到任何数据的。我们只能从 iTunes 的备份中，导出微信 App 的数据，然后通过分析数据，实现一系列的功能（比如导出聊天记录，数据计算等等）。

## TODO

- support non-text record type
- add avatars group members
