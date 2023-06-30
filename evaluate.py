# -*- coding:utf-8 -*-
# Author:   xiayouran
# Email:    youran.xia@foxmail.com
# Datetime: 2023/6/29 10:54
# Filename: evaluate.py
import imageio
import numpy as np
import multiprocessing as mp
import time

from clean_watermark import CleanWater


def calculate_time(num_executions=10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            total_time = np.zeros(shape=num_executions)
            for i in range(num_executions):
                start_time = time.time()
                func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                total_time[i] = execution_time
                print("The function [{}] run time: {:.4f} s".format(func.__name__, execution_time))

            print("The function [{}] run average time: {:.4f} s".format(func.__name__, total_time[1:-1].mean()))

        return wrapper

    return decorator


@calculate_time(num_executions=10)
def clean_watermark_no_multiprocess():
    img_file = 'imgs/logo-watermark.jpg'
    img_data = imageio.imread(img_file)
    height, width, channel = img_data.shape

    if channel == 3:
        fill_color = np.asarray([254, 255, 255], dtype=np.uint8)
    else:
        fill_color = np.asarray([254, 255, 255, 255], dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            rgb_data = img_data[i, j]
            if CleanWater.rgb2hex(rgb_data) in CleanWater.watermark_color:
                img_data[i, j] = fill_color

    imageio.imsave('imgs/logo.png', img_data)


@calculate_time(num_executions=10)
def clean_watermark_with_multiprocess():
    img_file = 'imgs/logo-watermark.jpg'
    img_data = imageio.imread(img_file)
    cpu_num = mp.cpu_count()
    img_blocks = CleanWater.split_img(img_data)

    pool = mp.Pool(processes=cpu_num)
    img_blocks = pool.map(CleanWater.clean_water, img_blocks)
    img_data_clean = CleanWater.merge_img(img_blocks)

    assert img_data_clean.shape == img_data.shape, 'img_data_clean and img_data must have the same shape'

    imageio.imsave('imgs/logo.png', img_data_clean)


if __name__ == '__main__':
    clean_watermark_no_multiprocess()
    clean_watermark_with_multiprocess()
