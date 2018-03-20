#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
from Board import Board
from Disc import Disc
from PlayerObject import PlayerObject
from Player import Player
from AI import AI

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

        # clicked out of the board
        if(mouse.x > 720):
            return

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

        p1_status = self.Player1.placeDisc(self.Board, self.Turn, self.clicked_board_index)
        p2_status = self.Player2.placeDisc(self.Board, self.Turn, self.clicked_board_index)

        if(p1_status == "Pass"):
            self.pass_count += 1
            self.Turn = "Black" if (self.Turn == "White") else "White"
        elif(p1_status == "Done"):
            self.pass_count = 0
            self.Turn = "Black" if (self.Turn == "White") else "White"
        
        if(p2_status == "Pass"):
            self.pass_count += 1
            self.Turn = "Black" if (self.Turn == "White") else "White"
        elif(p2_status == "Done"):
            self.pass_count = 0
            self.Turn = "Black" if (self.Turn == "White") else "White"

        self.draw()

        if(self.pass_count < 2):
            self.root.after(10, self.play)
