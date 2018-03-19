#!/usr/bin/python3
# -*- coding: utf8 -*-
from PlayerObject import PlayerObject


class Player(PlayerObject):

    def __init__(self, myTurn):
        super().__init__(myTurn)