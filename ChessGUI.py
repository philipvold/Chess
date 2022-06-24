## -*- coding: utf-8 -*-
# """
# Created on Tue Sep  6 00:10:26 2016
#
# @author: Philip
# """
#
from tkinter import Tk, PhotoImage, Text, Button, INSERT, Label

from AI_v1 import *
from AI_v2 import *
from SkakMat2 import Board


def create_btn(row, col, color, img=Empt):
    btn = Button(Chess, bg=color, image=img, command=lambda: position(row, col))
    btn.grid(row=row, column=col)


def get_color(row, column):
    color1 = "white"
    color2 = "brown"
    if row % 2 == column % 2:
        clr = color1
    else:
        clr = color2
    return clr


def get_img(i, j):
    if i == 0:
        if j in [0, 7]:
            img = BR
        elif j in [1, 6]:
            img = BK
        elif j in [2, 5]:
            img = BB
        elif j == 3:
            img = BQn
        else:
            img = BKi
    elif i == 1:
        img = BP
    elif i == 6:
        img = WP
    elif i == 7:
        if j in [0, 7]:
            img = WR
        elif j in [1, 6]:
            img = WK
        elif j in [2, 5]:
            img = WB
        elif j == 3:
            img = WQn
        else:
            img = WKi
    else:
        img = Empt
    return img


def start_game():
    for i in range(8):
        for j in range(8):
            B[i][j] = create_btn(i, j, get_color(i, j), get_img(i, j))


def position(i, j):
    CB.find_legal_moves()
    c = None
    if not move[4]:
        move[0] = i
        move[1] = j
        move[4] = True
    elif move[4]:
        move[2] = i
        move[3] = j
        move[4] = False
        c = CB.state[move[0]][move[1]]
        moves = CB.moves
    if c != None:
        textbox.delete(1.0, END)
        if (c.color == "W" and CB.wt) or (c.color == "B" and not CB.wt):
            Mtype = CB.legal_moves[c.color][c][(move[2], move[3])]
            c.move_piece(move[2], move[3])
            if moves != CB.moves:
                c = CB.state[move[2]][move[3]]  # Update piece if promoted pawn
                if CB.wt == True:
                    CB.wt = False
                    chg_turn(CB.wt)
                else:
                    CB.wt = True
                    chg_turn(CB.wt)
                img = imgur[c.Ctype]
                B[move[0]][move[1]] = create_btn(
                    move[0], move[1], get_color(move[0], move[1]), Empt
                )
                B[move[2]][move[3]] = create_btn(
                    move[2], move[3], get_color(move[2], move[3]), img
                )
                
                if Mtype in ["passant", "short castling", "long castling"]:
                    if c.color == "W":
                        if Mtype == "passant":
                            B[move[2] + 1][move[3]] = create_btn(
                                move[2] + 1,
                                move[3],
                                get_color(move[2] + 1, move[3]),
                                Empt,
                            )
                        elif Mtype == "short castling":
                            B[7][5] = create_btn(7, 5, get_color(7, 5), WR)
                            B[7][7] = create_btn(7, 7, get_color(7, 7), Empt)
                        else:
                            B[7][2] = create_btn(7, 3, get_color(7, 3), WR)
                            B[7][0] = create_btn(7, 0, get_color(7, 0), Empt)
                    if c.color == "B":
                        if Mtype == "passant":
                            B[move[2] - 1][move[3]] = create_btn(
                                move[2] - 1,
                                move[3],
                                get_color(move[2] - 1, move[3]),
                                Empt,
                            )
                        elif Mtype == "short castling":
                            B[0][5] = create_btn(0, 5, get_color(0, 5), BR)
                            B[0][7] = create_btn(0, 7, get_color(0, 7), Empt)
                        else:
                            B[0][2] = create_btn(0, 3, get_color(0, 3), BR)
                            B[0][0] = create_btn(0, 0, get_color(0, 0), Empt)
        else:
            print("It is not even your turn!")


def chg_turn(turn):
    if turn:
        Label(text="Turn: White", bg="white").grid(row=6, column=9)
    else:
        Label(text="Turn: Black", bg="brown").grid(row=6, column=9)


def move_aidan():
    i = 0
    thisTurn = CB.moves
    while CB.moves == thisTurn and i <= 50:
        moveAidan = Aidan.best_move(2)
        moveAidan.append(True)
        position(moveAidan[0], moveAidan[1])
        position(moveAidan[2], moveAidan[3])
        i += 1


def get_incumbent(is_white):
    if is_white:
        incumbentScore = -1000
    else:
        incumbentScore = 1000
    return incumbentScore


def move_bent():
    Bent.board.betaBentMove = True
    startScore = get_incumbent(CB.wt)
    moveBent = Bent.bestMove(CB.wt, startScore)
    moveBent.append(True)
    position(moveBent[0], moveBent[1])
    position(moveBent[2], moveBent[3])
    print("Material: ", Bent.materialScore(), " move ", Bent.moveScore(), " pawns ", Bent.pawnPosition(),)
    CB.print_board()
    Bent.board.betaBentMove = False


""" Print to GUI as well as console """


def decorator(func):
    def inner(inputStr):
        try:
            textbox.insert(INSERT, inputStr)
            return func(inputStr)
        except:
            return func(inputStr)
    
    return inner


if __name__ == '__main__':
    
    CB = Board()
    Chess = Tk()
    Chess.title("SkakMat2")
    
    textbox = Text(Chess)
    textbox.grid(row=0, column=8, columnspan=6, rowspan=5)
    
    move = [0, 0, 0, 0, False]
    
    B = [["X"] * 8] * 8
    """ Images """
    img_path = "C:\\Users\\Philip\\Dropbox\\Python\\cp\\"
    BP = PhotoImage(file=f"{img_path}BP.png", height=80)
    BK = PhotoImage(file=f"{img_path}BK.png", height=80)
    BB = PhotoImage(file=f"{img_path}BB.png", height=80)
    BQn = PhotoImage(file=f"{img_path}BQn.png", height=80)
    BKi = PhotoImage(file=f"{img_path}BKi.png", height=80)
    BR = PhotoImage(file=f"{img_path}BR.png", height=80)
    WP = PhotoImage(file=f"{img_path}WP.png", height=80)
    WK = PhotoImage(file=f"{img_path}WK.png", height=80)
    WB = PhotoImage(file=f"{img_path}WB.png", height=80)
    WQn = PhotoImage(file=f"{img_path}WQn.png", height=80)
    WKi = PhotoImage(file=f"{img_path}WKi.png", height=80)
    WR = PhotoImage(file=f"{img_path}WR.png", height=80)
    Empt = PhotoImage(file=f"{img_path}Empty.png", height=80, width=80)
    
    imgur = {}
    for col in ['B', 'W']:
        for pc in ['P', 'K', 'B', 'Qn', 'Ki', 'R']:
            imgur[f"{col}{pc}"] = PhotoImage(file=f"{img_path}{col}{pc}.png", height=80)
    
    Label(text="Turn: White", bg="white").grid(row=6, column=9)
    
    Button(Chess, bg="blue", text="AIdan", height=4, width=10, command=lambda: move_aidan()).grid(row=6, column=10)
    Button(Chess, bg="red", text="BetaBent", height=4, width=10, command=lambda: move_bent()).grid(row=6, column=8)
    
    Aidan = AI1(CB)
    Bent = BetaBent(CB)
    start_game()
    
    Chess.mainloop()
