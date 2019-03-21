# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/21 16:49
# @File   : login_weixin.py
from handle.wechat_handle import WeChatPCLoginHandle


class WeChatAPI(object):
    def login_wechat(self):
        wx = WeChatPCLoginHandle()
        # wx.handle_full_screen_shot(image_file_name='login.png')
        wx.click_login()


if __name__ == '__main__':
    wechat = WeChatAPI()
    wechat.login_wechat()
