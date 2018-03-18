#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import sys


class GameManager(object):
    canvas = None
    Board = None
    Player1 = None
    Player2 = None
    Turn = None

    def __init__(self, Board, Player1, Player2):
        self.frame = tk.Frame(width=960, height=720)
        self.frame.place(x=0, y=0)
        self.canvas = tk.Canvas(self.frame, width=720, height=720)
        self.canvas.place(x=0, y=0)

        self.Board = Board
        self.Player1 = Player1
        self.Player2 = Player2

    def click(self, mouse):
        print(mouse.x, mouse.y)
        self.canvas.delete("disc")  # ボード上の石を消す
        self.draw()
        self.canvas.create_oval(mouse.x - 44, mouse.y - 44, mouse.x + 44, mouse.y + 44, fill="Black", outline="Black", tag="disc")

    def draw(self, ):
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
        for index, disc in enumerate(self.Board.discs):
            center_x = 45 + int((index-1) % 10) * 90
            center_y = 45 + int((index-10) / 10) * 90
            if(disc.type == "Black"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="Black", outline="Black", tag="disc")
            elif(disc.type == "White"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="White", outline="Black", tag="disc")
            elif(disc.type == "CanPlace"):    
                self.canvas.create_oval(center_x - 6, center_y - 6, center_x + 6, center_y + 6, fill="OliveDrab1", outline="OliveDrab1", tag="disc")
            # 最後に打たれた石の場合、マークを付ける
            if(disc.newest_place):
                self.canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="Red", outline="Red", tag="disc")

        self.canvas.pack()


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

    def __init__(self,):
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


def main():
    Player1 = None # プレーヤー1
    Player2 = None # プレーヤー2

    args = sys.argv # コマンドライン引数
    if(len(args) >= 3):
        Player1 = Player() if args[1] == '-player' else AI() if args[1] == '-ai' else None
        Player2 = Player() if args[2] == '-player' else AI() if args[2] == '-ai' else None
    elif(len(args) == 2):
        Player1 = AI() if args[1] == '-training' else None
        Player2 = AI() if args[1] == '-training' else None
    if(Player1 is None or Player2 is None):
            args = []

    if(len(args) < 2):
        print("error!!")
        print("If you want to play Player vs Player mode, execute below command")
        print(" $python main.py -player -player")
        print("")
        print("If you want to play Player vs AI mode, execute below command")
        print(" $python main.py -player -ai")
        print("")
        print("If you want to play AI vs AI mode, execute below command")
        print(" $python main.py -ai -ai")
        print("")
        print("If you want to play AI training mode, execute below command")
        print(" $python main.py -training")
        print("")
        sys.exit()

    root = tk.Tk()  # rootウィンドウを作成
    root.title("AlphaRe")  # rootウィンドウのタイトルを変える
    root.geometry("960x720")  # rootウィンドウの大きさを960x720に
    root.resizable(0, 0)  # 縦、横共に画面サイズの変更を禁止

    board = Board() # ボードクラス 
    gameManager = GameManager(board, Player1, Player2) # ゲームマネージャークラス
    gameManager.draw()

    # 左クリックしたときのコールバック関数motionを呼び出す
    root.bind("<Button-1>", gameManager.click)

    root.mainloop()  # メインループ


if __name__ == '__main__':
    main()
