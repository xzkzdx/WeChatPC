# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py

from handle import Handle, InvalidHandleError


class WeChatMainWndForPCLoginHandle(Handle):
    class_name = "WeChatLoginWndForPC"
    class_titles = ["登录", '微信']

    def __init__(self):
        for title_index, class_title in enumerate(self.class_titles):
            self.class_title = class_title
            try:
                super().__init__(self.class_name, self.class_title)
                break
            except InvalidHandleError:
                if title_index == len(self.class_titles):
                    raise InvalidHandleError("没有登陆窗口，请确认您的操作")
        self.change_position(None, None, 280, 400)

    def change_position(self, *args):
        self.reset_handle_rect(*args)

    def wx_handle(self):
        """获取微信句柄"""
        return self.handle

    def first_login(self):
        """第一次登陆"""
        pass

    def login(self):
        """登陆"""
        self.left_click_position(140, 280)


class WeChatMainWndForPCHandle(Handle):
    class_name = "WeChatMainWndForPC"
    class_title = "微信"

    def __init__(self):
        super().__init__(self.class_name, self.class_title)

    def wx_handle(self):
        """获取微信句柄"""
        return self.handle


if __name__ == '__main__':
    wx = WeChatMainWndForPCLoginHandle()
    rect = wx.get_handle_rect()
    print(rect)
    wx.login()
