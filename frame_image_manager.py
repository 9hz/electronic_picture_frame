#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ghz
@contact: ghz65535@163.com
@time: 2023-02-09
"""

import os
import random

from PIL import Image
from PIL.Image import Resampling


def is_image(path):
    try:
        return path.split('.')[-1].lower() in ['jpg', 'png', 'jpeg', 'gif']
    except:
        return False


class ImageManager:
    def __init__(self, width, height):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.width = width
        self.height = height
        self.image_dir = f'{self.current_dir}/images'
        self.preprocess_dir = f'{self.current_dir}/preprocess'
        self.image_path_pool = {}
        self.image_list = []
        self.last_path = None
        os.makedirs(self.image_dir, exist_ok=True)

    def _scan_images(self):
        """
        :return: whether the content of image dir have something changed
        """
        not_exist = []
        for path in self.image_path_pool:
            if not os.path.exists(path):
                not_exist.append(path)
        should_update = False
        if len(not_exist) > 0:
            should_update = True
            for path in not_exist:
                self.image_path_pool.pop(path)
        new_images = []
        for file in os.listdir(self.image_dir):
            if is_image(file):
                path = f'{self.image_dir}/{file}'
                if path not in self.image_path_pool:
                    new_images.append(path)
        if len(new_images) > 0:
            should_update = True
            for path in new_images:
                self.image_path_pool[path] = ''
        return should_update

    def _preprocess_image(self, path):
        os.makedirs(self.preprocess_dir, exist_ok=True)
        if self.image_path_pool[path] == '':
            filename = os.path.basename(path)
            new_file_path = f'{self.preprocess_dir}/{filename}'
            image = self._load_image(path)
            image.save(new_file_path)
            self.image_path_pool[path] = new_file_path
        return self.image_path_pool[path]

    def _load_image(self, path):
        image = Image.open(path)
        exif = image.getexif()
        key_Orientation = 0x0112
        if key_Orientation in exif:
            Orientation = exif[key_Orientation]
            # https://exiv2.org/tags.html
            if Orientation == 6:
                # angle: In degrees counter clockwise.
                image = image.rotate(270)
            elif Orientation == 3:
                image = image.rotate(180)
            elif Orientation == 8:
                image = image.rotate(90)
        image = self._crop_image(image)
        return image

    def _crop_image(self, image):
        """
        Enlarge or reduce the image with black edges so that it can be displayed on the screen
        :param image:
        :return: target image
        """
        w = image.width
        h = image.height
        if self.width * h == self.height * w:
            return image.resize((self.width, self.height), Image.ANTIALIAS)
        if self.width * h > self.height * w:
            # self.width / self.height > w / h
            target_width = w * self.height // h
            image = image.resize((target_width, self.height), Resampling.LANCZOS)
            target = Image.new('RGB', (self.width, self.height), 'black')
            target.paste(image, ((self.width - target_width) // 2, 0))
            return target
        if self.width * h < self.height * w:
            # self.width / self.height < w / h
            target_height = h * self.width // w
            image = image.resize((self.width, target_height), Resampling.LANCZOS)
            target = Image.new('RGB', (self.width, self.height), 'black')
            target.paste(image, (0, (self.height - target_height) // 2))
            return target

    def pick_image(self):
        """
        :return: preprocessed image path
        """
        should_update = self._scan_images()
        if len(self.image_list) == 0 or should_update:
            self.image_list = list(self.image_path_pool.keys())
            random.shuffle(self.image_list)
        path = self.image_list.pop()
        if path == self.last_path:
            path = self.image_list.pop()
        self.last_path = path
        return self._preprocess_image(path)
