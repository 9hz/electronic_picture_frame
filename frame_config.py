#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ghz
@contact: ghz65535@163.com
@time: 2023-02-09
"""

import os
from configparser import ConfigParser


class Config:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = f'{self.current_dir}/config.txt'
        self.last_mtime = 0
        self.debug = True
        self.prefetch_max_size = 10
        self.interval = 60
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file_path):
            mtime = os.path.getmtime(self.config_file_path)
            if self.last_mtime != mtime:
                self.last_mtime = mtime
                parser = ConfigParser()
                parser.read(self.config_file_path)
                self.debug = parser.getboolean('default', 'debug', fallback=True)
                self.interval = parser.getint('default', 'prefetch_max_size', fallback=10)
                self.interval = parser.getint('default', 'interval', fallback=60)
