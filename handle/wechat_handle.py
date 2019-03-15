# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
import time

from handle import Handle, InvalidHandleError


class WeChatPCLoginHandle(Handle):
    class_name = "WeChatLoginWndForPC"
    class_titles = ["登录", '微信']
    default_width = 280
    default_height = 400

    def __init__(self):
        for title_index, class_title in enumerate(self.class_titles, start=1):
            self.class_title = class_title
            try:
                super().__init__(self.class_name, self.class_title)
                break
            except InvalidHandleError:
                if title_index == len(self.class_titles):
                    self.load_error("没有登陆窗口，请确认您的操作")
        self.change_position(None, None, self.default_width, self.default_height)

    def first_login(self):
        """第一次登陆"""
        pass

    def login(self):
        """登陆"""
        self.show_handle()
        self.mouse_left_click_position(140, 280)
        self.check_login()

    def check_login(self):
        """登录验证"""
        while 1:
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatMainWndForPC", '微信'):
                    break
            self.show_handle()
            break


class WeChatPCHandle(Handle):
    class_name = "WeChatMainWndForPC"
    class_title = "微信"
    default_width = 850
    default_height = 560

    def __init__(self):
        super().__init__(self.class_name, self.class_title)
        self.change_position(None, None, self.default_width, self.default_height)

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

    def menu_more(self):
        self.show_handle()
        self.mouse_left_click_position(30, 535)
        menu_handle = WeChatPCMenuHandle()
        print(menu_handle.handler)


class WeChatPCMenuHandle(Handle):
    class_name = 'SetMenuWnd'
    class_title = ""
    default_width = 134
    default_height = 138

    def __init__(self):
        super().__init__(self.class_name, self.class_title)
        self.change_position(None, None, self.default_width, self.default_height)


class WeChatPCLogoutHandle(Handle):
    class_name = "ConfirmDialog"
    class_title = "微信"
    default_width = 360
    default_height = 224

    def __init__(self):
        super().__init__(self.class_name, self.class_title)
        self.change_position(None, None, self.default_width, self.default_height)

    def logout(self):
        """退出登陆"""
        self.set_handle_foreground()
        self.show_handle()
        self.mouse_left_click_position(225, 190)
        # self.mouse_left_click_position(self.left + 190, self.top + 225)
        self.check_logout()

    def check_logout(self):
        """退出登录验证"""
        while 1:
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatLoginWndForPC", '微信'):
                    break
                # self.show_handle()
                # color = self.get_position_color(self.left + 64, self.top + 98)
                # print(color)
            break


if __name__ == '__main__':
    # wx = WeChatPCLogoutHandle()
    # wx.logout()
    wx = WeChatPCHandle()
    wx.menu_more()
    # wx = WeChatPCLoginHandle()
    # wx.login()

    # print(wx.handler)
    # wx.handle_full_screen_shot(image_file_name='img.png')
    # wx.hidden_handle()
    # wx.show_handle()
    # wx.message_list_move2top()
    # wx.message_list_move2bottom()
