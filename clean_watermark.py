# -*- coding:utf-8 -*-
# Author:   xiayouran
# Email:    youran.xia@foxmail.com
# Datetime: 2023/6/14 16:16
# Filename: clean_watermark.py
import imageio
import numpy as np
from PIL import Image
import multiprocessing as mp


class CleanWater(object):
    watermark_color = [
        '#FCFDFD', '#F6F7F7', '#F5F6F6', '#F7F8F8', '#FDFEFE', '#F8F9F9', '#F9FAFA', '#FAFBFB', '#FBFCFC', '#F3F4F4',
        '#EFF0F0', '#F1F2F2', '#F0F1F1', '#F4F5F5', '#F2F3F3', '#FCFCFC', '#F6F6F6', '#FAFAFA', '#FDFDFD', '#FEFEFE',
        '#F7F7F7', '#FBFBFB', '#F5F5F5', '#F1F1F1', '#F0F0F0', '#F8F8F8', '#F4F4F4', '#F2F2F2', '#F9F9F9', '#F3F3F3'
    ]

    @classmethod
    def rgb2hex(cls, rgb_value):
        hex_str = [str(hex(d))[2:] for d in rgb_value[:3]]
        hex_str = '#' + ''.join(hex_str)

        return hex_str.upper()

    @classmethod
    def clean_water(cls, img_data):
        height, width, channel = img_data.shape
        if channel == 3:
            fill_color = np.asarray([254, 255, 255], dtype=np.uint8)
        else:
            fill_color = np.asarray([254, 255, 255, 255], dtype=np.uint8)

        for i in range(height):
            for j in range(width):
                rgb_data = img_data[i, j]
                if cls.rgb2hex(rgb_data) in cls.watermark_color:
                    img_data[i, j] = fill_color

        return img_data

    @classmethod
    def split_img(cls, img_data, interval=32):
        height, width, channel = img_data.shape
        num_block = height // interval + 1
        img_blocks = np.array_split(img_data, num_block, axis=0)

        return img_blocks

    @classmethod
    def merge_img(cls, img_data_blocks):
        img_data = np.concatenate(img_data_blocks, axis=0)

        return img_data


if __name__ == '__main__':
    img_file = 'imgs/logo-watermark.jpg'
    img_data = imageio.imread(img_file)
    cpu_num = mp.cpu_count()
    img_blocks = CleanWater.split_img(img_data)

    pool = mp.Pool(processes=cpu_num)
    img_blocks = pool.map(CleanWater.clean_water, img_blocks)
    img_data_clean = CleanWater.merge_img(img_blocks)

    assert img_data_clean.shape == img_data.shape, 'img_data_clean and img_data must have the same shape'

    imageio.imsave('imgs/logo.png', img_data_clean)

    # img = Image.fromarray(img_data)
    # img.save('imgs/logo.png', quality=95)
