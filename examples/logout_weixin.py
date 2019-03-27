# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/27 14:57
# @File   : logout_weixin.py
from handle.wechat_handle import WeChatPCLoginHandle, WeChatPCHandle, WeChatSettingWndHandle


class WeChatAPI(object):
    def login_wechat(self):
        wx = WeChatPCLoginHandle()
        wx.click_login()

    def logout_wechat(self):
        """对已登录进行退出登录"""
        wx = WeChatPCHandle()
        wx.get_menu_setting()

        wx_setting = WeChatSettingWndHandle()
        wx_setting.click_logout()


if __name__ == '__main__':
    wechat = WeChatAPI()
    wechat.logout_wechat()
