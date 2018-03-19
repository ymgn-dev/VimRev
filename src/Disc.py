#!/usr/bin/python3
# -*- coding: utf8 -*-


class Disc(object):

    type = None  # 石の種類(空き : "Space", 黒 : "Black", 白 : "White", 着手可能場所 : "CanPlace", 番兵 : "Ban")
    newest_place = False  # 最後に打たれた石ならTrue

    def __init__(self, type=None, newest_place=False):
        self.type = type
        self.newest_place = newest_place