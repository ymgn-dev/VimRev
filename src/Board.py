#!/usr/bin/python3
# -*- coding: utf8 -*-
from Disc import Disc


class Board(object):

    discs = None  # ボード上の石(ディスク)

    def __init__(self,):
        # 石や番兵を配置
        self.discs = []
        for i in range(100):
            d = Disc()
            self.discs.append(d)

        # Initialize board
        self.Initialize()

    # ボードを初期化
    def Initialize(self, ):
        for i in range(0, 10):
            self.discs[i].type = "Ban"
            self.discs[i + 90].type = "Ban"
        for i in range(10, 81, 10):
            self.discs[i].type = "Ban"
            self.discs[i + 9].type = "Ban"
        for i in range(0, 90):
            if(int(i / 10) == 0 or int(i % 10) == 0 or int(i % 10) == 9):
                continue
            else:
                self.discs[i].type = "Space"

        self.discs[45].type = "Black"
        self.discs[54].type = "Black"
        self.discs[44].type = "White"
        self.discs[55].type = "White"
        self.discs[34].type = "CanPlace"
        self.discs[43].type = "CanPlace"
        self.discs[56].type = "CanPlace"
        self.discs[65].type = "CanPlace"

    # ボード上の着手可能場所に印を付けて着手可能場所のリストを返す
    def getCanPlace(self, turn):

        # 着手可能場所の印を全て消す
        for index, disc in enumerate(self.discs):
            if(disc.type == "CanPlace"):
                self.discs[index].type = "Space"

        list_canplace = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8方向探索
        myDisc = "Black" if (turn == "Black") else "White"
        yourDisc = "Black" if (turn == "White") else "White"

        for index, disc in enumerate(self.discs):
            if (disc.type == "Space"):
                for d in direction:
                    if (self.discs[index + d].type == yourDisc):
                        k = index + d * 2
                        while(True):
                            if(self.discs[k].type == "Ban" or self.discs[k].type == "Space" or self.discs[k].type == "CanPlace"):
                                break
                            elif(self.discs[k].type == myDisc):
                                self.discs[index].type = "CanPlace"
                                list_canplace.append(index)
                                break
                            k += d
        return list_canplace

    # 最後に置かれた石の印を消す
    def resetNewDisc(self, ):
        for index, disc in enumerate(self.discs):
            if(disc.newest_place):
                self.discs[index].newest_place = False

    # 着手する場所に石を置き、周りの石をひっくり返す
    def reverseDisc(self, turn, index):
        
        list_reverse = []
        direction = [-11, -10, -9, -1, +1, +9, +10, +11] # 8方向探索
        myDisc = "Black" if (turn == "Black") else "White"
        yourDisc = "Black" if (turn == "White") else "White"

        for d in direction:
            j = index + d
            while(True):
                if(self.discs[j].type == yourDisc):
                    list_reverse.append(j)
                elif(self.discs[j].type == myDisc):
                    for rev in list_reverse:
                        self.discs[rev].type = myDisc
                    break
                elif(self.discs[j].type == "Space" or self.discs[j].type == "CanPlace" or self.discs[j].type == "Ban"):
                    list_reverse = []
                    break
                j+= d

        self.discs[index].type = myDisc
        self.discs[index].newest_place = True