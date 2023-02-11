#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ghz
@contact: ghz65535@163.com
@time: 2023-02-09
"""

import datetime
import os
import threading
import tkinter as tk

from PIL import ImageTk


class FrameUI:
    def __init__(self, config):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config = config
        self.window = None
        self.canvas = None
        self.width = None
        self.height = None
        self.tk_image = None
        self.tk_text_location = None
        self.tk_text_time = None
        self.lock = threading.Lock()
        self.prefetch = []
        self.last_show_image_time = 0
        self.last_text = None
        self._init_ui()

    def _init_ui(self):
        window = tk.Tk()
        if self.config.debug:
            width = window.winfo_screenwidth() // 2
            height = window.winfo_screenheight() // 2
        else:
            window.attributes('-fullscreen', True)
            window.config(cursor='none')
            width = window.winfo_screenwidth()
            height = window.winfo_screenheight()

        if self.config.debug:
            print(f'window={width}x{height}')

        canvas = tk.Canvas(window, bg='black', width=width, height=height,
                           borderwidth=0, highlightthickness=0)
        canvas.pack()
        self.window = window
        self.canvas = canvas
        self.width = width
        self.height = height

    def _show_image(self):
        """
        :return: whether a new image is displayed
        """
        current = datetime.datetime.now()
        current_time = current.timestamp()
        if current_time - self.last_show_image_time >= self.config.interval:
            with self.lock:
                if len(self.prefetch) > 0:
                    self.tk_image = self.prefetch.pop(0)
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
                    self.last_show_image_time = current_time
                    return True
        return False

    def _show_time(self, force=False):
        current = datetime.datetime.now()
        current_text = current.strftime("%H:%M")
        if force or current_text != self.last_text:
            self.canvas.delete('text_time')
            self.tk_text_time = self.canvas.create_text(self.width - 30, 30, anchor=tk.NE, fill='white',
                                                        font=('Helvetica', '120', 'bold'),
                                                        tag='text_time',
                                                        text=f'{current_text}')
            self.canvas.update()
            self.last_text = current_text

    def should_add_prefetch_image(self):
        with self.lock:
            return len(self.prefetch) <= self.config.prefetch_max_size

    def add_prefetch_image(self, path):
        tk_image = ImageTk.PhotoImage(file=path)
        with self.lock:
            self.prefetch.append(tk_image)

    def on_schedule(self):
        new_image_displayed = self._show_image()
        self._show_time(force=new_image_displayed)
        self.window.after(1000, self.on_schedule)

    def start(self):
        self.on_schedule()
        tk.mainloop()
