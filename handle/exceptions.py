# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/14 11:17
# @File   : exceptions.py


class InvalidHandleError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


