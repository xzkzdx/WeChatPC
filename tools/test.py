# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/15 13:31
# @File   : test.py

from PIL.Image import open


img = open('img.png')
print(img.getbands(), img.size)
# img.show()
