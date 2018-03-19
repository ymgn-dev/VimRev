#!/usr/bin/python3
# -*- coding: utf8 -*-


class PlayerObject(object):

    myTurn = None
    def __init__(self, myTurn):
        self.myTurn = myTurn

    def placeDisc(self, board, global_turn, b_index,):

        # 着手可能場所を取得
        list_canplace = board.getCanPlace(self.myTurn)

        # 自分のターンじゃないときは何もしない
        if(self.myTurn != global_turn or b_index is None):
            return "None"

        # 着手できる場所が無いときはパス
        if(len(list_canplace) == 0):
            return "Pass"

        # クリックした場所に着手可能なとき
        if(board.discs[b_index].type == "CanPlace"):
            board.resetNewDisc()
            board.reverseDisc(self.myTurn, b_index)
            return "Done"