#!/usr/bin/python3
# -*- coding: utf8 -*-
from PlayerObject import PlayerObject
import random


class AI(PlayerObject):

    def __init__(self, myTurn):
        super().__init__(myTurn)

    def placeDisc(self, board, global_turn, b_index,):
        # 自分のターンじゃないときは何もしない
        if(self.myTurn != global_turn):
            return "None"
        
        list_canplace = board.getCanPlace(self.myTurn)
        # 着手できる場所が無いときはパス
        if(len(list_canplace) == 0):
            return "Pass"

        # 着手可能な場所からランダムに選択して打つ
        random.shuffle(list_canplace) # 着手可能場所のリストをランダムにシャッフル
        board.resetNewDisc()
        board.reverseDisc(self.myTurn, list_canplace[0])
        return "Done"