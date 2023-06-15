# -*- coding:utf-8 -*-
# Author:   xiayouran
# Email:    youran.xia@foxmail.com
# Datetime: 2023/6/14 16:16
# Filename: clean_watermark.py
import imageio
import numpy as np
from PIL import Image


def rgb2hex(rgb_value):
    hex_str = [str(hex(d))[2:] for d in rgb_value[:3]]
    hex_str = '#' + ''.join(hex_str)

    return hex_str.upper()


watermark_color = [
    '#FCFDFD', '#F6F7F7', '#F5F6F6', '#F7F8F8', '#FDFEFE', '#F8F9F9', '#F9FAFA', '#FAFBFB', '#FBFCFC', '#F3F4F4',
    '#EFF0F0', '#F1F2F2', '#F0F1F1', '#F4F5F5', '#F2F3F3', '#FCFCFC', '#F6F6F6', '#FAFAFA', '#FDFDFD', '#FEFEFE',
    '#F7F7F7', '#FBFBFB', '#F5F5F5', '#F1F1F1', '#F0F0F0', '#F8F8F8', '#F4F4F4', '#F2F2F2', '#F9F9F9', '#F3F3F3'
]


if __name__ == '__main__':
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
            if rgb2hex(rgb_data) in watermark_color:
                img_data[i, j] = fill_color

    imageio.imsave('imgs/logo.png', img_data)

    # img = Image.fromarray(img_data)
    # img.save('imgs/logo.png', quality=95)
