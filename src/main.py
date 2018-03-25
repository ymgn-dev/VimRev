#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
import sys
import argparse

from GameManager import GameManager
from Board import Board
from Disc import Disc
from PlayerObject import PlayerObject
from Player import Player
from AI import AI


def main():

    # parser
    parser = argparse.ArgumentParser(description='VimRev')
    parser.add_argument('-f', '--first', help='select first move', choices=['player', 'ai'], required=True)
    parser.add_argument('-p', '--passive', help='select passive move', choices=['player', 'ai'], required=True)

    # コマンドライン引数の解析
    args = parser.parse_args()
    Player1 = Player("Black") if args.first == 'player' else AI("Black")
    Player2 = Player("White") if args.passive == 'player' else AI("White")

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
