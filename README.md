# 功能特性
微信PC版自动化API

# 安装
依赖第三方库： pywin32  PIL

pip install pywin32 

pip install PIL

推荐git clone直接下载WeChatPC项目，部署到自己的程序中即可。

在原有基础上，可以按需求进行功能扩充。

目前仅支持Windows版，Mac端请配置对应句柄。

欢迎爱好者fork共同开发。


# example示例

login_weixin.py 

```
# -*- encoding: utf-8 -*-
#在没有启动微信PC的情况下自动启动WeChat，并根据是否扫码选择点击登录，显示二维码等登录操作。
from handle.wechat_handle import WeChatPCLoginHandle, WeChatStartUp


class WeChatAPI(object):
    def login_wechat(self):
        wx = WeChatPCLoginHandle()
        wx.click_login()


if __name__ == '__main__':
    WeChatStartUp('C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe').startup()
    wechat = WeChatAPI()
    wechat.login_wechat()

```