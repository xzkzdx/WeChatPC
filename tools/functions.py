# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/15 13:45
# @File   : functions.py
import os

from PIL import Image
from settings import ABS_DIR_PATH, IMAGE_DIR_NAME


def get_img_pix_color(abs_png_path, x_position=0, y_position=0):
    """获取图片指定像素点的像素"""
    img_src = Image.open(abs_png_path)
    img_src = img_src.convert('RGBA')
    rgd_color = img_src.load()[x_position, y_position]
    img_src.close()
    return rgd_color


def make_dir(dir_path, dir_name):
    """创建文件夹"""
    if not os.path.exists(os.path.join(dir_path, dir_name)):
        os.mkdir(os.path.join(dir_path, dir_name))


def path_join(*path):
    return os.path.join(ABS_DIR_PATH, *path)


if __name__ == '__main__':
    color = get_img_pix_color(path_join('image', 'img.png'))
    print(color)
    print(ABS_DIR_PATH)
    make_dir(ABS_DIR_PATH, IMAGE_DIR_NAME)
    print(path_join('image', 'img.png'))
    print()
