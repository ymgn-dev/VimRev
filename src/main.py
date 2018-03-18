#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import sys


class GameManager(object):

    root = None
    frame = None
    canvas = None
    Board = None
    Player1 = None
    Player2 = None
    Turn = None
    clicked_board_index = None
    pass_count = None

    def __init__(self, root, Board, Player1, Player2):
        self.root = root
        self.frame = tk.Frame(width=960, height=720)
        self.frame.place(x=0, y=0)
        self.canvas = tk.Canvas(self.frame, width=720, height=720)
        self.canvas.place(x=0, y=0)

        self.Board = Board
        self.Player1 = Player1
        self.Player2 = Player2

        self.Turn = "Black"
        self.pass_count = 0

        # 左クリック時にコールバック関数self.clickを呼び出す
        self.root.bind("<Button-1>", self.click)
    
    # ボードの着手可能場所を全て"空き"にする
    def clean_board(self, ):
        for index, disc in enumerate(self.Board.discs):
            if(disc.type == "CanPlace"):
                self.Board.discs[index].type = "Space"

    def click(self, mouse):
        # print(mouse.x, mouse.y)
        index = int(mouse.y / 90 + 1) * 10 + int(mouse.x / 90 + 1)
        self.clicked_board_index = index

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

        # ボードの丸印を描画
        self.canvas.create_oval(180 - 4, 180 - 4, 180 + 4, 180 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(180 - 4, 540 - 4, 180 + 4, 540 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(540 - 4, 180 - 4, 540 + 4, 180 + 4, fill="Black", outline="Black", tag="board")
        self.canvas.create_oval(540 - 4, 540 - 4, 540 + 4, 540 + 4, fill="Black", outline="Black", tag="board")

        # 石を描画
        for index, disc in enumerate(self.Board.discs):
            center_x = 45 + int((index-1) % 10) * 90
            center_y = 45 + int((index-10) / 10) * 90
            if(disc.type == "Black"):    
                self.canvas.create_oval(center_x - 43, center_y - 43, center_x + 43, center_y + 43, fill="Black", outline="Black", tag="disc")
            elif(disc.type == "White"):    
                self.canvas.create_oval(center_x - 44, center_y - 44, center_x + 44, center_y + 44, fill="White", outline="Black", tag="disc")
            elif(disc.type == "CanPlace"):    
                self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="OliveDrab1", outline="OliveDrab1", tag="disc")
            # 最後に打たれた石の場合、マークを付ける
            if(disc.newest_place):
                self.canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="Red", outline="Red", tag="disc")

        self.canvas.pack()

        # コンソール出力テスト
        '''
        print(len(self.Board.discs))
        for index, disc in enumerate(self.Board.discs):
            str = " " if index % 10 != 9 else '\n'
            if(disc.type == "Ban"):
                print("@" + str, end="")
            elif(disc.type == "Space"):
                print("*" + str, end="")
            elif(disc.type == "Black"):
                print("o" + str, end="")
            elif(disc.type == "White"):
                print("x" + str, end="")
            else:
                print("?" + str, end="")
        '''

    def play(self, ):

        # 着手可能場所を全て消す
        # self.clean_board()

        player1_status = self.Player1.placeDisc(self.Board, self.Turn, self.clicked_board_index)
        player2_status = self.Player2.placeDisc(self.Board, self.Turn, self.clicked_board_index)

        if(player1_status == "Pass"):
            self.pass_count += 1
            self.Turn = "Black" if (self.Turn == "White") else "White"
        elif(player1_status == "Done"):
            self.pass_count = 0
            self.Turn = "Black" if (self.Turn == "White") else "White"
        
        if(player2_status == "Pass"):
            self.pass_count += 1
            self.Turn = "Black" if (self.Turn == "White") else "White"
        elif(player2_status == "Done"):
            self.pass_count = 0
            self.Turn = "Black" if (self.Turn == "White") else "White"
        
        self.draw()

        if(self.pass_count < 2):
            self.root.after(10, self.play)


class PlayerObject(object):

    myTurn = None
    def __init__(self, myTurn):
        self.myTurn = myTurn

    def placeDisc(self, board, global_turn, b_index):
        # 自分のターンじゃないときは何もしない
        if(self.myTurn != global_turn or b_index is None):
            return "None"

        list_canplace = board.getCanPlace(self.myTurn)
        # 着手できる場所が無いときはパス
        if(len(list_canplace) == 0):
            return "Pass"

        # クリックした場所に着手可能なとき
        if(board.discs[b_index].type == "CanPlace"):
            # board.discs[b_index].type = self.myTurn
            board.resetNewDisc()
            board.reverseDisc(self.myTurn, b_index)
            return "Done"


class Player(PlayerObject):

    def __init__(self, myTurn):
        super().__init__(myTurn)


class AI(PlayerObject):

    def __init__(self, myTurn):
        super().__init__(myTurn)


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


def main():

    Player1 = None # プレーヤー1
    Player2 = None # プレーヤー2

    args = sys.argv # コマンドライン引数
    if(len(args) >= 3):
        Player1 = Player("Black") if args[1] == '-player' else AI("Black") if args[1] == '-ai' else None
        Player2 = Player("White") if args[2] == '-player' else AI("White") if args[2] == '-ai' else None
    elif(len(args) == 2):
        Player1 = AI("Black") if args[1] == '-training' else None
        Player2 = AI("White") if args[1] == '-training' else None
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
    gameManager = GameManager(root, board, Player1, Player2) # ゲームマネージャークラス
    root.after(10, gameManager.play)

    root.mainloop()  # メインループ


if __name__ == '__main__':
    main()
