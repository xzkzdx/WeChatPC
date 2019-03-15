# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
import time

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
        self.change_position(None, None, 280, 400, not_ensure_move=False)

    def wx_handle(self):
        """获取微信句柄"""
        return self.handle

    def first_login(self):
        """第一次登陆"""
        pass

    def login(self):
        """登陆"""
        self.mouse_left_click_position(140, 280)


class WeChatMainWndForPCHandle(Handle):
    class_name = "WeChatMainWndForPC"
    class_title = "微信"

    def __init__(self):
        super().__init__(self.class_name, self.class_title)
        self.change_position(200, 100, 850, 560)

    def wx_handle(self):
        """获取微信句柄"""
        return self.handle

    def message_list_move2top(self):
        position_x = self.left + 305
        position_y = self.top + 100
        self.mouse_left_click_move(position_x, position_y, position_x, position_y + 100)

        # self.message_list_range_move(10000)

    def message_list_move2bottom(self):
        self.message_list_range_move(10000, move_up=False)
        # position_x = self.left + 180
        # position_y = self.top + 150
        # color = self.get_position_color(position_x, position_y)
        # print(color)

    def message_list_range_move(self, frequency: int, move_up: bool = True):
        self.show_handle()
        time.sleep(0.1)
        position_x = self.left + 180
        position_y = self.top + 150
        for i in range(frequency):
            self.mouse_move_up(position_x, position_y) if move_up else self.mouse_move_down(position_x, position_y)
        self.hidden_handle()


if __name__ == '__main__':
    # wx = WeChatMainWndForPCLoginHandle()
    # wx.login()
    wx = WeChatMainWndForPCHandle()
    rect = wx.get_handle_rect()
    print(rect)
    # wx.hidden_handle()
    # wx.show_handle()
    wx.message_list_move2top()
    # wx.message_list_move2bottom()
