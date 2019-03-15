# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/14 10:29
# @File   : handle.py

import win32gui
import win32api
import win32ui

import win32con
import time
import win32clipboard
from win32api import GetSystemMetrics
from PIL import ImageGrab


class InvalidHandleError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Handle(object):
    def __init__(self, handle_class_name, handle_title):
        self.handle = win32gui.FindWindow(handle_class_name, handle_title)
        if self.handle == 0:
            raise InvalidHandleError('无效的窗口句柄。')
        self.left, self.top, self.width, self.height = self.get_handle_rect()

    def check_handle(self, handle_class_name, handle_title):
        """验证句柄"""
        return win32gui.FindWindow(handle_class_name, handle_title) != 0

    def create_handle_dc(self):
        """根据窗口句柄获取窗口的设备上下文DC（Divice Context）"""
        return win32gui.GetWindowDC(self.handle)

    def create_handle_mfc_dc(self, dc=None):
        """根据窗口上下文创建dc"""
        return win32ui.CreateDCFromHandle(dc if dc else self.create_handle_dc())

    def handle_compatible_dc(self, dc=None, mfc_dc=None):
        """根据mfcDC创建可兼容的DC"""
        dc = dc if dc else self.create_handle_dc()
        mfc_dc = mfc_dc if mfc_dc else self.create_handle_mfc_dc(dc)
        return mfc_dc.CreateCompatibleDC()

    def handle_full_image(self, dc=None, mfc_dc=None, compatible_dc=None, image_file_name=''):
        """句柄截图"""
        dc = dc if dc else self.create_handle_dc()
        mfc_dc = mfc_dc if mfc_dc else self.create_handle_mfc_dc(dc=dc)
        compatible_dc = compatible_dc if compatible_dc else self.handle_compatible_dc(dc=dc, mfc_dc=mfc_dc)
        save_bit_map = win32ui.CreateBitmap()  # 创建bigmap准备保存图片
        # 句柄全大小
        full_screen_width, full_screen_height = int(self.width * 1.5), int(self.height * 1.5)
        full_size = (full_screen_width, full_screen_height)
        # 为bitmap开辟空间
        save_bit_map.CreateCompatibleBitmap(mfc_dc, full_screen_width, full_screen_height)
        # 高度saveDC，将截图保存到saveBitmap中
        compatible_dc.SelectObject(save_bit_map)
        compatible_dc.BitBlt((0,0), full_size, mfc_dc, (0,0), win32con.SRCCOPY)
        # compatible_dc.BitBlt((0, 0), (self.width*2, self.height*2), mfc_dc, (71, 121), win32con.SRCCOPY)
        # 目标矩形顶点(0,0)长宽(w,h),源设备mfcDC,源矩形顶点tmptl
        rtns = save_bit_map.GetBitmapBits()
        if image_file_name:
            save_bit_map.SaveBitmapFile(compatible_dc, image_file_name)
        return rtns

    @property
    def handler(self):
        """获取句柄"""
        return self.handle

    def get_handle_rect(self):
        """获取句柄矩形"""
        # abs_position = win32gui.GetWindowRect(self.handle)[:2]
        abs_position = win32gui.GetWindowPlacement(self.handle)[-1][:2]
        handle_shape = win32gui.GetClientRect(self.handle)[2:]
        # print(abs_position, handle_shape)
        return abs_position + handle_shape

    def reset_handle_rect(self, *rect, not_ensure_move=False):
        """rect must has four params,
        example: (left, top, width, height)
        if any param is None or lt zero, it will not change
        """
        for r_ in rect:
            if not (isinstance(r_, int)) ^ (r_ is None):
                raise ValueError("reset_rect() params must be int or None")
        if len(rect) != 4:
            raise TypeError("reset_rect() takes exactly 4 arguments (%s given)" % len(rect))
        self.left = self.left if rect[0] is None else rect[0]
        self.top = self.top if rect[1] is None else rect[1]
        self.width = self.width if rect[2] is None else rect[2]
        self.height = self.height if rect[3] is None else rect[3]
        win32gui.MoveWindow(self.handle, self.left, self.top, self.width, self.height, not_ensure_move)

    def change_position(self, *args, not_ensure_move: bool = False, ensure_hidden: bool = True):
        self.show_handle()
        self.reset_handle_rect(*args, not_ensure_move=not_ensure_move)
        self.set_handle_min() if ensure_hidden else self.set_handle_foreground()

    def set_handle_max(self):
        """最大化句柄窗口"""
        # self.set_handle_min()
        win32gui.ShowWindow(self.handle, win32con.SW_MAXIMIZE)

    def set_handle_min(self):
        """最小化句柄窗口"""
        win32gui.ShowWindow(self.handle, win32con.SW_MINIMIZE)

    def show_handle(self):
        """显示句柄窗口"""
        win32gui.ShowWindow(self.handle, win32con.SW_SHOWDEFAULT)
        # self.set_handle_background()

    def hidden_handle(self):
        """隐藏句柄窗口  0 """
        # win32gui.ShowWindow(self.handle, win32con.HIDE_WINDOW)
        win32gui.ShowWindow(self.handle, win32con.SW_HIDE)

    def set_handle_foreground(self):
        """在前台显示"""
        # self.show_handle()
        win32gui.SetForegroundWindow(self.handle)

    def set_handle_background(self):
        """在后台显示"""
        win32gui.SetForegroundWindow(self.handle)

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

    def mouse_left_click_move(self, x_position, y_position, x_end_position, y_end_position, sleep_time=1):
        # 将两个16位的值连接成一个32位的地址坐标
        start_position = win32api.MAKELONG(x_position, y_position)
        end_position = win32api.MAKELONG(x_end_position, y_end_position)
        self.set_mouse_position(x_position, y_position)
        time.sleep(int(sleep_time))
        # 点击左键
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_position)
        self.set_mouse_position(x_end_position, y_end_position)
        time.sleep(int(sleep_time))
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x_position, y_position, 1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, -1)
        time.sleep(int(sleep_time))
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, end_position)
        time.sleep(int(sleep_time))

    def mouse_right_click_position(self, x_position, y_position, sleep_time=0.1):
        """鼠标右点击"""
        # 将两个16位的值连接成一个32位的地址坐标
        long_position = win32api.MAKELONG(x_position, y_position)
        # 点击左键
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)
        time.sleep(int(sleep_time))

    def mouse_left_click_position(self, x_position, y_position, sleep_time=0.1):
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

    def mouse_move_up(self, x_position, y_position):
        self.set_mouse_position(x_position, y_position)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x_position, y_position, 1)

    def mouse_move_down(self, x_position, y_position):
        self.set_mouse_position(x_position, y_position)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)

    def get_screen_resolution(self):
        return GetSystemMetrics(0), GetSystemMetrics(1)

    def get_position_color(self, x_position, y_position):
        s_width, s_height = self.get_screen_resolution()  # Python获取屏幕分辨率
        # im = ImageGrab.grab((0, 0, s_height, s_height))  # 与坐标不同，这里0，0，1，1是一个像素，而坐标是从0~1919的
        # pix = im.load()
        # return pix[x_position, y_position]
        return ImageGrab.grab((0, 0, s_width, s_height)).load()[x_position, y_position]


if __name__ == '__main__':
    print(ImageGrab.grab((0, 0, GetSystemMetrics(0), GetSystemMetrics(1))).load()[1, 0])
