# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/21 16:49
# @File   : login_weixin.py
from handle.wechat_handle import WeChatPCLoginHandle, WeChatStartUp


class WeChatAPI(object):
    def login_wechat(self):
        wx = WeChatPCLoginHandle()
        wx.click_login()


if __name__ == '__main__':
    WeChatStartUp('C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe').startup()
    wechat = WeChatAPI()
    wechat.login_wechat()
