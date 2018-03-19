#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import sys

from GameManager import GameManager
from Board import Board
from Disc import Disc
from PlayerObject import PlayerObject
from Player import Player
from AI import AI


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
    root.title("VimRev")  # rootウィンドウのタイトルを変える
    root.geometry("960x720")  # rootウィンドウの大きさを960x720に
    root.resizable(0, 0)  # 縦、横共に画面サイズの変更を禁止

    board = Board() # ボードクラス 
    gameManager = GameManager(root, board, Player1, Player2) # ゲームマネージャークラス
    gameManager.play()

    root.mainloop()  # メインループ


if __name__ == '__main__':
    main()
