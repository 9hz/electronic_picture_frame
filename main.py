#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ghz
@contact: ghz65535@163.com
@time: 2023-02-09
"""
import threading
import time

from frame_config import Config
from frame_hour_reporting import HourReporting
from frame_image_manager import ImageManager
from frame_ui import FrameUI


def timer_task():
    while True:
        config.load_config()
        if ui.should_add_prefetch_image():
            path = manager.pick_image()
            ui.add_prefetch_image(path)
        time.sleep(1)


if __name__ == '__main__':
    config = Config()
    ui = FrameUI(config)
    manager = ImageManager(ui.width, ui.height)
    HourReporting()
    timer_thread = threading.Thread(target=timer_task)
    timer_thread.start()
    ui.start()
