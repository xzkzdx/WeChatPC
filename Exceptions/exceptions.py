# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/14 11:17
# @File   : exceptions.py


class InvalidHandleError(Exception):
    """无效的句柄异常"""

    def __init__(self, *args):
        super(InvalidHandleError, self).__init__(*args)
