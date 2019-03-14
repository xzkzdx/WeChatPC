# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 10:48
# @File   : wechat_windows.py

import win32gui
import win32api
import win32con
import time
import win32clipboard


def right_click_position(hwd, x_position, y_position, sleep_time):
    """鼠标右点击"""
    # 将两个16位的值连接成一个32位的地址坐标
    long_position = win32api.MAKELONG(x_position, y_position)
    # 点击左键
    win32api.SendMessage(hwd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, long_position)
    win32api.SendMessage(hwd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, long_position)
    time.sleep(int(sleep_time))


def left_click_position(hwd, x_position, y_position, sleep_time):
    """鼠标左点击"""
    # 将两个16位的值连接成一个32位的地址坐标
    long_position = win32api.MAKELONG(x_position, y_position)
    # 点击左键
    win32api.SendMessage(hwd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
    win32api.SendMessage(hwd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
    time.sleep(sleep_time)


def get_text_from_clipboard():
    """读取剪切板"""
    win32clipboard.OpenClipboard()
    d = win32clipboard.GetClipboardData(win32con.CF_TEXT)
    win32clipboard.CloseClipboard()
    return d.decode('gbk')


def set_text_to_clipboard(string):
    """写入剪切板"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, string.encode(encoding='gbk'))
    win32clipboard.CloseClipboard()


def get_mouse_position():
    """获取鼠标位置"""
    return win32api.GetCursorPos()


def set_mouse_position(x_position, y_position):
    """设置鼠标位置"""
    return win32api.SetCursorPos((x_position, y_position))


def input_content(hwd, content, sleep_second):
    """粘贴到消息发送框"""
    # 存入粘贴板
    set_text_to_clipboard(content)
    # 鼠标右键调 WeChatMainWndForPC 的 CMenuWnd 粘贴板
    right_click_position(hwd, 400, 500, 0.1)
    time.sleep(sleep_second)
    # 获取 CMenuWnd 粘贴板句柄
    CMenuWnd = win32gui.FindWindow("CMenuWnd", "CMenuWnd")
    # 鼠标左击粘贴
    left_click_position(CMenuWnd, 20, 10, 0.1)
    # click_combination_keys(hwd, win32con.VK_CONTROL, win32con.VK_RETURN)


def click_single_key(hwd, key):
    """模拟键盘独立按键"""
    win32api.SendMessage(hwd, win32con.WM_KEYDOWN, key, 0)
    win32api.SendMessage(hwd, win32con.WM_KEYUP, key, 0)


def click_multi_keys(hwd, *key):
    """模拟键盘多个独立按键"""
    for k in key:
        click_single_key(hwd, k)


def click_combination_keys(hwd, *args):
    """模拟键盘组合按键"""
    for arg in args:
        print(arg)
        win32api.SendMessage(hwd, win32con.WM_SYSKEYDOWN, arg, 0)
    for arg in args:
        win32api.SendMessage(hwd, win32con.WM_SYSKEYUP, arg, 0)


def weixin_operation(hwd, msg):
    # 点击联系人
    left_click_position(hwd, 200, 100, 0.1)
    # 写入消息
    input_content(hwd, msg, 0.1)


if __name__ == "__main__":
    # 查找句柄
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")
    # 查找指定句柄的子句柄，后两个参数为子类的类名与标题，如果没有或不确定，可以写None
    # hwnd = win32gui.FindWindow(hwnd, None, None, None)
    if int(hwnd) <= 0:
        print("没有找到模拟器，退出进程................")
        exit(0)
    print("查询到模拟器句柄: %s " % hwnd)
    # 没有直接修改窗口大小的方式，但可以曲线救国，几个参数分别表示句柄,起始点坐标,宽高度,是否重绘界面
    # 如果想改变窗口大小，就必须指定起始点的坐标，没果对起始点坐标没有要求，随便写就可以；
    print(win32gui.GetWindowPlacement(hwnd)[-1])
    hwnd_rect = win32gui.GetWindowPlacement(hwnd)[-1]
    # 如果还想要放在原先的位置，就需要先获取之前的边框位置，再调用该方法即可
    win32gui.MoveWindow(hwnd, hwnd_rect[0], hwnd_rect[1], 850, 560, )
    # win32gui.MoveWindow(hwnd, hwnd_rect[0], hwnd_rect[1], hwnd_rect[2], hwnd_rect[3], True)
    # time.sleep(2)
    # 屏幕坐标到客户端坐标
    # print(win32gui.ScreenToClient(hwnd, (1446, 722)))
    # 设置为前台
    win32gui.SetForegroundWindow(hwnd)
    # 设置为后台
    # win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)
    # time.sleep(2)
    # 下列的后三个参数分别表示: 文件路径 打招呼句子 广告语
    for i in range(5):
        weixin_operation(hwnd, '连续发送成功次数 %s' % i)
