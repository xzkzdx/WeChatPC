# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
import time

import pywintypes

from handle import Handle, InvalidHandleError
from settings import LOGIN_UPDATE_TIME, ERROR_IGNORE_TIME
from tools.functions import exists_exe


class WeChatStartUp(Handle):

    def __init__(self, exe_path: str = '', exe_name: str = 'WeChat.exe'):
        """先尝试将exe名加入初始化，若系统找不到指定文件，请尝试初始化exe的绝对路径
        如：exe_path = 'WeChat.exe'
        或：exe_path = 'C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe' """
        self.exe_path = exe_path
        self.exe_name = exe_name

    def startup(self):
        self.startup_exe(self.exe_path)
        while 1:
            if exists_exe(self.exe_name):
                break


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
        do_check = True
        first_check = True
        while 1:
            time.sleep(LOGIN_UPDATE_TIME)
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatMainWndForPC", '微信'):
                    break
            elif first_check:
                first_check = False
                for i in range(1, 15):
                    """斜向求值"""
                    try:
                        change_color = self.get_position_color(130 + i, 340 + i)
                    except pywintypes.error:
                        return
                    if change_color != (245, 245, 245, 255):
                        """全灰度判断"""
                        do_check = False
                        # print(130 + i, 340 + i)
                        break
                if do_check:
                    self.code_login()
                    do_check = False


class WeChatPCHandle(Handle):
    """WeChat父句柄"""

    def __init__(self):
        self.initial("WeChatMainWndForPC", "微信", *(None, None, 850, 560))

    def scroll_move2top(self, place='left', ):
        pass

    def scroll_move2button(self, place='left', ):
        pass

    def message_list_move2top(self):
        # position_x = self.left + 180
        # position_y = self.top + 100
        # self.mouse_left_click_move(position_x, position_y, position_x, position_y + 100)
        self.message_list_range_move(10000)

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
        # self.hidden_handle()

    def get_menu_setting(self):
        self.show_handle()
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        self.mouse_left_click_position(60, 115, handle_id=menu_handle_id)

    def get_menu_feedback(self):
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        self.mouse_left_click_position(60, 25, handle_id=menu_handle_id)

    def get_menu_backup_and_recovery(self):
        self.mouse_left_click_position(30, 535)
        menu_handle_id = self.get_handle_by_position(105, 470)
        self.mouse_left_click_position(60, 70, handle_id=menu_handle_id)

    def click_friend(self, f_position):
        self.mouse_left_click_position(170, f_position)

    def input_content(self, msg_content):
        """粘贴到消息发送框"""
        # 存入粘贴板
        self.set_text_to_clipboard(msg_content)
        # 鼠标右键调 WeChatMainWndForPC 的 CMenuWnd 粘贴板
        self.mouse_right_click_position(400, 500)
        # 获取 CMenuWnd 粘贴板句柄
        c_menu_wnd = CMenuWnd()
        # 鼠标左击粘贴
        c_menu_wnd.click_menu_wnd()
        # click_combination_keys(hwd, win32con.VK_CONTROL, win32con.VK_RETURN)

    def send_msg2dialog_box(self, msg_content):
        """粘贴到消息发送框"""
        self.mouse_left_click_position(450, 500)
        # 存入粘贴板
        self.set_text_to_clipboard(msg_content)
        # 鼠标右键调 WeChatMainWndForPC 的 CMenuWnd 粘贴板
        self.mouse_right_click_position(400, 500, 0.1)
        # 获取 CMenuWnd 粘贴板句柄
        c_menu_wnd = CMenuWnd()
        # 鼠标左击粘贴
        c_menu_wnd.click_menu_wnd()

    def send_msg2friend(self, msg_content, f_position: int):
        self.click_friend(f_position)
        self.send_msg2dialog_box(msg_content)
        self.mouse_left_click_position(780, 540)

    def send_msg2top_friend(self, msg_content):
        self.message_list_move2top()
        self.click_friend(90)
        self.send_msg2dialog_box(msg_content)
        self.mouse_left_click_position(780, 540)

    def click_sending_msg(self, m_position):
        self.mouse_left_click_position(710, m_position)

    def close_web_view(self, wait_time: float):
        web_view = WeChatWebViewWnd()
        web_view.close_web(wait_time)


class WeChatChatWnd(Handle):
    """微信聊天句柄"""

    def __init__(self, name: str):
        self.initial("ChatWnd", name, *(None, None, 550, 640))

    def send_msg(self, msg_content):
        """发送消息"""
        self.show_handle()
        self.set_handle_foreground()
        # 存入粘贴板
        self.set_text_to_clipboard(msg_content)
        # 鼠标右键调 WeChatMainWndForPC 的 CMenuWnd 粘贴板
        self.mouse_right_click_position(200, 580, 0.1)
        # 获取 CMenuWnd 粘贴板句柄
        c_menu_wnd = CMenuWnd()
        # 鼠标左击粘贴
        c_menu_wnd.click_menu_wnd()
        # 点击发送
        self.mouse_left_click_position(self.width - 60, self.height - 20)

    def click_last_sent_msg(self, m_position):
        self.mouse_left_click_position(710, m_position)

    def close_web_view(self, wait_time: float):
        web_view = WeChatWebViewWnd()
        web_view.close_web(wait_time)

    def move2bottom(self):
        self.message_list_range_move(10000, move_up=False)

    def close_chat(self):
        self.mouse_left_click_position(self.left - 15, 15)

    def message_list_range_move(self, frequency: int, move_up: bool = True):
        self.show_handle()
        time.sleep(0.1)
        position_x = self.left + 180
        position_y = self.top + 150
        for i in range(frequency):
            self.mouse_move_up(position_x, position_y) if move_up else self.mouse_move_down(position_x, position_y)
        # self.hidden_handle()

    def delete_top_msg(self):
        """删除顶条信息"""
        self.show_handle()
        self.set_handle_foreground()
        self.mouse_right_click_position(self.width - 90, 120, 0.1)
        time.sleep(1)
        # 获取 CMenuWnd 粘贴板句柄
        c_menu_wnd = CMenuWnd(None, None, 76, 196)
        # 鼠标左击粘贴
        c_menu_wnd.click_menu_wnd(t_position=c_menu_wnd.height - 5, sleep_time=0)
        # time.sleep(1)
        # 线程解决退出登录鼠标左键无法抬起的问题
        while 1:
            try:
                delete_h = WeChatPCLogoutHandle()
                delete_h.confirm()
                break
            except InvalidHandleError:
                continue


class CMenuWnd(Handle):
    """微信对话框粘贴板"""

    def __init__(self, *rect):
        rect = rect if rect else (None, None, 76, 30,)
        self.initial("CMenuWnd", "CMenuWnd", *rect)

    def click_menu_wnd(self, t_position: int = 10, sleep_time: float = 0):
        self.mouse_left_click_position(20, t_position, sleep_time)


class WeChatPCMenuHandle(Handle):
    """左下角菜单子句柄"""

    def __init__(self, handle_id, father_handle_id):
        """初始化菜单句柄id"""
        self.handle_id = handle_id
        self.father_handle_id = father_handle_id

    def click_feedback(self, message):
        """点击选择意见反馈"""
        self.mouse_left_click_position(60, 25, handle_id=self.handle_id)

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


class WeChatWebViewWnd(Handle):
    def __init__(self):
        self.initial('CefWebViewWnd', '微信', *(None, None, 640, 740))

    def close_web(self, wait_time: float = 0.1):
        self.mouse_left_click_position(625, 15, wait_time)


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

    def confirm(self):
        """确定"""
        self.set_handle_foreground()
        self.show_handle()
        self.mouse_left_click_position(225, 190)

    def logout(self):
        """退出登陆"""
        self.confirm()
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
    # wx = WeChatPCLoginHandle()
    # wx.click_login()
    # wx = WeChatPCHandle()
    # wx.send_msg2top_friend('http://baidu.com')
    # wx.click_sending_msg(380)
    # wx.close_web_view(5)
    # web_v = WeChatWebViewWnd()
    # print(web_v.handle)
    friend = WeChatChatWnd('清竹')
    friend.send_msg('https://mp.weixin.qq.com/s/hWKlgb_dGn9EO6lbQ7esHw')
    # friend.delete_top_msg()
