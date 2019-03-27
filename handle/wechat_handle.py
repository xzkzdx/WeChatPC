# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
import time

from handle import Handle, InvalidHandleError
from settings import LOGIN_UPDATE_TIME, ERROR_IGNORE_TIME


class WeChatPCLoginHandle(Handle):
    """WeChat登录句柄"""

    def __init__(self):
        class_titles = ["登录", '微信']
        for title_index, class_title in enumerate(class_titles, start=1):
            try:
                self.initial("WeChatLoginWndForPC", class_title, *(None, None, 280, 400))
                break
            except InvalidHandleError:
                if title_index == len(class_titles):
                    self.load_error("没有登陆窗口，请确认您的操作")

    def code_login(self, relative_x=140, relative_y=280):
        """二维码登陆"""
        self.handle_full_screen_shot(image_file_name='code_login.png')
        self.show_screen_shot(key_function=self.check_login, key_params=(relative_x, relative_y))

    def click_login(self, relative_x=140, relative_y=280):
        """点击登陆按钮登录"""
        self.show_handle()
        login_color = self.get_position_color(relative_x, relative_y, image_name='click_login.png')
        if login_color == (26, 173, 25, 255):
            self.mouse_left_click_position(relative_x, relative_y)
        self.check_login(relative_x, relative_y)

    def check_login(self, relative_x, relative_y):
        """登录验证"""
        self.show_handle()
        while 1:
            time.sleep(LOGIN_UPDATE_TIME)
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatMainWndForPC", '微信'):
                    break
            else:
                login_color = self.get_position_color(relative_x, relative_y)
                if login_color != (26, 173, 25, 255):
                    self.code_login()


class WeChatPCHandle(Handle):
    """WeChat父句柄"""

    def __init__(self):
        self.initial("WeChatMainWndForPC", "微信", *(None, None, 850, 560))

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

    def get_menu_setting(self):
        self.show_handle()
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        print(menu_handle_id)
        self.mouse_left_click_position(60, 115, handle_id=menu_handle_id)

    def get_menu_feedback(self):
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        print(menu_handle_id)
        self.mouse_left_click_position(60, 25, handle_id=menu_handle_id)

    def get_menu_backup_and_recovery(self):
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        print(menu_handle_id)
        self.mouse_left_click_position(60, 70, handle_id=menu_handle_id)


class WeChatPCMenuHandle(Handle):
    """左下角菜单子句柄"""

    def __init__(self, handle_id, father_handle_id):
        """初始化菜单句柄id"""
        self.handle_id = handle_id
        self.father_handle_id = father_handle_id

    def click_feedback(self, message):
        """点击选择意见反馈"""
        self.mouse_left_click_position(60, 25, handle_id=self.handle_id)
        print(message)

    def click_backup_and_recovery(self):
        """点击选择备份与恢复"""
        self.mouse_left_click_position(60, 70, handle_id=self.handle_id)

    def click_setting(self):
        """点击选择设置"""
        self.mouse_left_click_position(60, 115, handle_id=self.handle_id)


class WeChatPCFeedbackHandle(Handle):
    """意见反馈句柄"""

    def __init__(self):
        self.initial("SetMenuWnd", "", *(None, None, 134, 138))

    def feedback(self, message):
        self.set_text_to_clipboard(message)
        self.show_handle()
        self.mouse_left_click_position(100, 100)
        self.ctrl_v()


class WeChatSettingWndHandle(Handle):
    def __init__(self):
        self.initial('SettingWnd', '设置', *(None, None, 550, 470))

    def click_logout(self):
        """点击退出登录"""
        import threading
        self.show_handle()
        # 线程解决退出登录鼠标左键无法抬起的问题
        mouse_left = threading.Thread(target=self.mouse_left_click_position, args=(282, 282,))
        mouse_left.start()
        while 1:
            try:
                confirm_dialog = WeChatPCLogoutHandle()
                threading.Thread(target=confirm_dialog.logout).start()
                break
            except InvalidHandleError:
                time.sleep(ERROR_IGNORE_TIME)


class WeChatPCLogoutHandle(Handle):
    """WeChat退出登录句柄"""

    def __init__(self):
        self.initial("ConfirmDialog", "微信", *(None, None, 360, 224))

    def logout(self):
        """退出登陆"""
        self.set_handle_foreground()
        self.show_handle()
        self.mouse_left_click_position(225, 190)
        # self.mouse_left_click_position(self.left + 190, self.top + 225)
        self.check_logout()

    def cancel(self):
        self.set_handle_foreground()
        self.show_handle()
        self.set_mouse_position(self.left + 305, self.top + 190)
        self.mouse_left_click_position(305, 190)

    def check_logout(self):
        """退出登录验证"""
        while 1:
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatLoginWndForPC", '微信'):
                    break


if __name__ == '__main__':
    # wx = WeChatPCLogoutHandle()
    # wx.logout()
    wx = WeChatPCLoginHandle()
    # wx.handle_full_screen_shot(image_file_name='login.png')
    wx.click_login()

    wx = WeChatPCHandle()
    wx.get_menu_setting()
    # wx.get_menu().click_feedback('hello wechat')
    # wx_setting = WeChatSettingWndHandle()
    # wx_setting.click_logout()
    # confirm_dialog = WeChatPCLogoutHandle()
    # confirm_dialog.cancel()
