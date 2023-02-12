#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ghz
@contact: ghz65535@163.com
@time: 2023-02-11
"""
import collections
import datetime
import os
import random
import pygame


def play_mp3(path):
    if not path:
        return
    try:
        # stop previous music
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path)
        # https://www.pygame.org/docs/ref/music.html
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
    except Exception as e:
        print(e)
        pass


class HourReporting:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.clock_dir = f'{self.current_dir}/hour_reporting'
        self.clock_mp3 = collections.defaultdict(set)
        self.last_play_clock_time = 0
        self.scan_clock_mp3()
        pygame.init()

    def scan_clock_mp3(self):
        for i in range(24):
            target_dir = f'{self.clock_dir}/{i:02}'
            os.makedirs(target_dir, exist_ok=True)
            for file in os.listdir(target_dir):
                if file.endswith('.mp3'):
                    self.clock_mp3[i].add(f'{self.clock_dir}/{i:02}/{file}')

    def check_and_report(self):
        current = datetime.datetime.now()
        current_time = current.timestamp()
        if current_time - self.last_play_clock_time >= 5:
            weekday = current.weekday()
            hour = current.hour
            minute = current.minute
            second = current.second
            # Working day: 7am to 11pm
            # Non-working day: 9am to 11pm
            if (0 <= weekday <= 4 and 7 <= hour <= 23) or (5 <= weekday <= 6 and 9 <= hour <= 23):
                if minute == 0 and 0 <= second <= 2:
                    play_mp3(random.choice(list(self.clock_mp3[hour])))
                    self.last_play_clock_time = current_time
                    self.scan_clock_mp3()
