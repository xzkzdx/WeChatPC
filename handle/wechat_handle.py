# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
from handle.handle import Handle


class WeChatMainWndForPCHandle(Handle):
    def __init__(self):
        super(Handle).__init__("WeChatMainWndForPC", "微信")

    def wx_handle(self):
        return self.handle


if __name__ == '__main__':
    print(TypeError("reset_rect() takes exactly 4 arguments (%s given)" % len('we')))
    wx = WeChatMainWndForPCHandle()
    wx.wx_handle()
