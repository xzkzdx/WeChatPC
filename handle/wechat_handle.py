# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
from handle import Handle


class WeChatMainWndForPCHandle(Handle):
    class_name = "WeChatMainWndForPC"
    class_title = "微信"

    def __init__(self):
        super().__init__(self.class_name, self.class_title)

    def wx_handle(self):
        return self.handle


if __name__ == '__main__':
    print(TypeError("reset_rect() takes exactly 4 arguments (%s given)" % len('we')))
    wx = WeChatMainWndForPCHandle()
    rect = wx.get_handle_rect()
    print(rect)
