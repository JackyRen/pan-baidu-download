#!/usr/bin/env python2
# coding=utf-8

import json
import urllib2
import logging

from config import global_config
from bddown_core import Pan, GetFilenameError


def export(links):
    for link in links:
        pan = Pan(link)
        count = 1
        while count != 0:
            link, filename, count = pan.info
            if not filename and not link:
                raise GetFilenameError("无法获取下载地址或文件名！")
            export_single(filename, link)


def export_single(filename, link):
    jsonrpc_path = global_config.jsonrpc
    if not jsonrpc_path:
        print "请设置config.ini中的jsonrpc选项"
        exit(1)
    jsonreq = json.dumps(
        [{
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "id": "qwer",
            "params": [
                [link],
                {
                    "out": filename,
                    "header": "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0"
                              "\r\nReferer:http://pan.baidu.com/disk/home"
                }]
        }]
    )
    logging.debug(jsonreq)
    try:
        req = urllib2.urlopen(jsonrpc_path, jsonreq)
    except urllib2.URLError:
        raise JsonrpcError("jsonrpc无法连接，请检查jsonrpc地址是否有误！")
    if req.code == 200:
        print "已成功添加到jsonrpc\n"


class JsonrpcError(Exception):
    pass
