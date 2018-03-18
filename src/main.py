#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import sys


class GameManager(object):
    Board = None
    Player1 = None
    Player2 = None
    Turn = None

    def __init__(self, Board, Player1, Player2):
        self.Board = Board
        self.Player1 = Player1
        self.Player2 = Player2


class PlayerObject(object):
    pass

class Player(PlayerObject):
    pass

class AI(PlayerObject):
    pass

class Disc(object):
    type = None  # 石の種類(空き : "Space", 黒 : "Black", 白 : "White", 着手可能場所 : "CanPlace", 番兵 : "Ban")
    newest_place = False  # 最後に打たれた石ならTrue

    def __init__(self, type=None, newest_place=False):
        self.type = type
        self.newest_place = newest_place


class Board(object):
    discs = None  # ボード上の石(ディスク)
    canvas = None # キャンバス

    def __init__(self, root):
        # コンストラクタ
        self.canvas = tk.Canvas(root, width=960, height=720) # キャンバスを初期化

        # 石や番兵を配置
        self.discs = []
        for i in range(100):
            d = Disc()
            self.discs.append(d)

        self.discs[45].type = "Black"
        self.discs[54].type = "Black"
        self.discs[44].type = "White"
        self.discs[55].type = "White"
        self.discs[34].type = "CanPlace"
        self.discs[43].type = "CanPlace"
        self.discs[56].type = "CanPlace"
        self.discs[65].type = "CanPlace"

    def draw(self):
        self.canvas.delete("board") # ボードを消す
        self.canvas.delete("disc")  # ボード上の石を消す

        # ボードを描画
        self.canvas.create_rectangle(0, 0, 720, 720, fill='#1E824C', tag="board")

        # ボードのマスを描画
        for i in range(9):
            self.canvas.create_line(
                i * 90, 0, i * 90, 720, width=1.2, fill="Black", tag="board")
            self.canvas.create_line(
                0, i * 90, 720, i * 90, width=1.2, fill="Black", tag="board")

        # 石を描画
        for index, disc in enumerate(self.discs):
            center_x = 45 + int((index-1) % 10) * 90
            center_y = 45 + int((index-10) / 10) * 90
            if(disc.type == "Black"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="Black", outline="Black", tag="disc")
            elif(disc.type == "White"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="White", outline="White", tag="disc")
            elif(disc.type == "CanPlace"):    
                self.canvas.create_oval(center_x - 6, center_y - 6, center_x + 6, center_y + 6, fill="Green3", outline="Green3", tag="disc")
            # 最後に打たれた石の場合、マークを付ける
            if(disc.newest_place):
                self.canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="Red", outline="Red", tag="disc")

        self.canvas.pack()


def pushed(self):
    if(self["text"] == "ボタン"):
        self["text"] = "押されたよ"
    elif(self["text"] == "押されたよ"):
        self["text"] = "ボタン"

def motion(mouse):
    print(mouse.x, mouse.y)

def main():

    args = sys.argv # コマンドライン引数
    if(len(args) < 2):
        print("error!!")
        print("If you want to play Player vs Player mode, execute below command")
        print(" $python main.py -Player -Player")
        print("")
        print("If you want to play Player vs AI mode, execute below command")
        print(" $python main.py -Player -AI")
        print("")
        print("If you want to play AI vs AI mode, execute below command")
        print(" $python main.py -AI -AI")
        print("")
        print("If you want to play AI training mode, execute below command")
        print(" $python main.py -training")
        print("")
        sys.exit()


    root = tk.Tk()  # rootウィンドウを作成
    root.title("AlphaRe")  # rootウィンドウのタイトルを変える
    root.geometry("960x720")  # rootウィンドウの大きさを960x720に
    root.resizable(0, 0)  # 縦、横共に画面サイズの変更を禁止

    # 左クリックしたときのコールバック関数motionを呼び出す
    root.bind("<Button-1>", motion)

    board = Board(root)
    board.draw()

    root.mainloop()  # メインループ


if __name__ == '__main__':
    main()
