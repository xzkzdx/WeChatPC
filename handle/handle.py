# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/14 10:29
# @File   : handle.py

import win32gui
import win32api
import win32con
import time
import win32clipboard


class Handle(object):
    def __init__(self, handle_class_name, handle_title):
        self.handle = win32gui.FindWindow(handle_class_name, handle_title)
        self.left, self.top, self.width, self.height = self.get_handle_rect()

    def get_handle_rect(self):
        """获取句柄矩形"""
        return win32gui.GetWindowPlacement(self.handle)[-1]

    def reset_handle_rect(self, *rect):
        """rect must has four params,
        example: (left, top, width, height)
        if param is None or lt zero, it will not change
        """
        for r_ in rect:
            if not isinstance(r_, int) or r_ is not None:
                raise ValueError("reset_rect() params must be int or None")
        if len(rect) != 4:
            raise TypeError("reset_rect() takes exactly 4 arguments (%s given)" % len(rect))
        self.left = self.left if rect[0] is None or rect[0] < 0 else rect[0]
        self.top = self.top if rect[1] is None or rect[1] < 0 else rect[1]
        self.width = self.width if rect[2] is None or rect[2] < 0 else rect[2]
        self.height = self.height if rect[3] is None or rect[3] < 0 else rect[3]
        win32gui.MoveWindow(self.handle, self.left, self.top, self.width, self.height, True)

    def show_handle(self):
        """在前台显示"""
        win32gui.SetForegroundWindow(self.handle)
        win32gui.ShowWindow(self.handle)

    def hidden_handle(self):
        """在后台显示"""
        win32gui.SetBkMode(self.handle, win32con.TRANSPARENT)

    def get_mouse_position(self):
        """获取鼠标位置"""
        return win32api.GetCursorPos()

    def set_mouse_position(self, x_position, y_position):
        """设置鼠标位置"""
        return win32api.SetCursorPos((x_position, y_position))

    def get_text_from_clipboard(self, decoding='gbk'):
        """读取剪切板"""
        win32clipboard.OpenClipboard()
        d = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        return d.decode(decoding)

    def set_text_to_clipboard(self, string, encoding='gbk'):
        """写入剪切板"""
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_TEXT, string.encode(encoding=encoding))
        win32clipboard.CloseClipboard()

    def right_click_position(self, x_position, y_position, sleep_time=0.1):
        """鼠标右点击"""
        # 将两个16位的值连接成一个32位的地址坐标
        long_position = win32api.MAKELONG(x_position, y_position)
        # 点击左键
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)
        time.sleep(int(sleep_time))

    def left_click_position(self, x_position, y_position, sleep_time=0.1):
        """鼠标左点击"""
        # 将两个16位的值连接成一个32位的地址坐标
        long_position = win32api.MAKELONG(x_position, y_position)
        # 点击左键
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
        time.sleep(sleep_time)

    def click_single_key(self, key):
        """模拟键盘独立按键"""
        win32api.SendMessage(self.handle, win32con.WM_KEYDOWN, key, 0)
        win32api.SendMessage(self.handle, win32con.WM_KEYUP, key, 0)

    def click_multi_keys(self, *keys):
        """模拟键盘多个独立按键"""
        for key in keys:
            self.click_single_key(key)

    def click_combination_keys(self, *args):
        """模拟键盘组合按键"""
        for arg in args:
            win32api.SendMessage(self.handle, win32con.WM_SYSKEYDOWN, arg, 0)
        for arg in args:
            win32api.SendMessage(self.handle, win32con.WM_SYSKEYUP, arg, 0)
