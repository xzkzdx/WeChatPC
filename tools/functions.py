# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/15 13:45
# @File   : functions.py
import os
import psutil
import time
from PIL import Image
from settings import ABS_DIR_PATH, IMAGE_DIR_NAME


def get_process():
    proc_info = {}
    for proc in psutil.process_iter():
        proc_info[proc.pid] = proc.name()
    return proc_info


def close_image(before_pids: dict, after_pids: dict):
    for pid, name in after_pids.items():
        if name not in before_pids.values():
            for proc in psutil.process_iter():
                if proc.pid == pid and 'hoto' in name:
                    proc.kill()


def exists_exe(exe_name):
    """判断可执行应用是否启动"""
    for proc in psutil.process_iter():
        if proc.name() == exe_name:
            return True
    return False


def close_process(func):
    def __inner(*args, **kwargs):
        before_process = get_process()
        f_result = func(*args, **kwargs)
        after_process = get_process()
        # print(len(before_process.keys()), len(after_process.keys()))
        close_image(before_process, after_process)
        return f_result

    return __inner


def get_img_pix_color(png_name, x_position=0, y_position=0):
    """获取图片指定像素点的像素"""
    img_src = Image.open(path_join(ABS_DIR_PATH, IMAGE_DIR_NAME, png_name))
    img_src = img_src.convert('RGBA')
    rgd_color = img_src.load()[x_position, y_position]
    img_src.close()
    return rgd_color


def exists_path(*file_name):
    return os.path.exists(path_join(ABS_DIR_PATH, *file_name))


@close_process
def show_image(png_name, key_function=None, key_params: tuple = None):
    img_src = Image.open(path_join(ABS_DIR_PATH, IMAGE_DIR_NAME, png_name))
    img_src.show()
    if key_function:
        key_function(*key_params)


def make_dir(dir_path, dir_name):
    """创建文件夹"""
    if not os.path.exists(os.path.join(dir_path, dir_name)):
        os.mkdir(os.path.join(dir_path, dir_name))


def path_join(*path):
    return os.path.join(ABS_DIR_PATH, *path)


if __name__ == '__main__':
    color = get_img_pix_color(path_join('image', 'login.png'), 210, 420)
    print(color)
    # print(ABS_DIR_PATH)
    # make_dir(ABS_DIR_PATH, IMAGE_DIR_NAME)
    # print(path_join('image', 'imag', 'img.png'))
    # print()
    show_image('login.png', key_function=lambda x: time.sleep(x), key_params=(1,))
