# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 15:37:02 2016

@author: Philip
"""

""" Test environment for SkakMat2 """
from SkakMat2 import *

testlist = []


def run_tests(testlist):
    maks = len(testlist)
    i = 1
    for tests in testlist:
        if tests:
            print("Test " + str(i) + " of " + str(maks) + " succeded")
            i += 1
        else:
            print("Test " + str(i) + " of " + str(maks) + " failed")
            break


def move_test(item, row, column):
    if item.board.state[row][column] == item:
        return True
    else:
        return False


""" CheckPath() """
BB = Board()
""" Empty paths """
testlist.append(BB.clear_path(3, 3, 5, 5))  # 001 True
testlist.append(BB.clear_path(5, 5, 3, 3))  # 002 True
testlist.append(BB.clear_path(2, 0, 2, 7))  # 003 True
testlist.append(BB.clear_path(2, 7, 2, 0))  # 004 True
testlist.append(BB.clear_path(1, 0, 6, 0))  # 005 True
testlist.append(BB.clear_path(6, 0, 1, 0))  # 006 True
BB.BP1.move_piece(2, 1)
testlist.append(BB.clear_path(0, 2, 2, 0))  # 007 True
""" Obstructed paths """
testlist.append(not BB.clear_path(1, 0, 7, 6))  # 008 False
testlist.append(not BB.clear_path(7, 6, 1, 0))  # 009 False
testlist.append(not BB.clear_path(3, 5, 7, 5))  # 010 False
testlist.append(not BB.clear_path(7, 5, 3, 5))  # 011 False
testlist.append(not BB.clear_path(1, 3, 1, 6))  # 012 False
testlist.append(not BB.clear_path(1, 6, 1, 3))  # 013 False
testlist.append(not BB.clear_path(1, 2, 3, 5))  # 014 False)

""" Testing pawns"""
BB = Board()
BB.WP1.move_piece(4, 1)
testlist.append(move_test(BB.WP1, 4, 1))  # 015 True
BB.WP1.move_piece(2, 1)
testlist.append(not move_test(BB.WP1, 2, 1))  # 016 False
BB.WP1.move_piece(3, 1)
testlist.append(move_test(BB.WP1, 3, 1))  # 017 True
BB.WP1.move_piece(2, 1)
BB.WP1.move_piece(1, 1)
testlist.append(not move_test(BB.WP1, 1, 1))  # 018 False
BB.WP1.move_piece(1, 0)
testlist.append(move_test(BB.WP1, 1, 0))  # 019 True
BB.WP1.move_piece(0, -1)
testlist.append(move_test(BB.WP1, 1, 0))  # 020 True
# BB.WP1.move_piece(0,1)
# testlist.append(not move_test(BB.WP1,0,1)) # 021 True ### TEST WILL FAIL WHEN CONVERSION IS ADDED TO THE GAME!!!
testlist.append(True)
BB.BP0.move_piece(2, 0)
testlist.append(not move_test(BB.BP0, 2, 0))  # 22 False
BB.BP1.move_piece(2, 1)
BB.BP2.move_piece(2, 1)
testlist.append(not move_test(BB.BP2, 2, 1))  # 023 False
BB.BP1.move_piece(3, 1)
BB.BP1.move_piece(4, 1)
BB.WP0.move_piece(4, 0)
BB.WP2.move_piece(4, 2)
BB.BP1.move_piece(5, 0)
testlist.append(not move_test(BB.BP1, 5, 0))  # 024 False
BB.BP1.move_piece(5, 2)
testlist.append(move_test(BB.BP1, 5, 2))  # 025 True
BB.WP3.move_piece(4, 3)
BB.WP3.move_piece(3, 3)
BB.BP3.move_piece(3, 3)
testlist.append(not move_test(BB.BP3, 3, 3))  # 026 False
BB.BP4.move_piece(3, 4)
BB.BP2.move_piece(3, 2)
BB.WP3.move_piece(2, 4)
testlist.append(not move_test(BB.WP3, 4, 2))  # 027 False
BB.WP3.move_piece(2, 2)
testlist.append(move_test(BB.WP3, 2, 2))  # 028 True


""" Testing knights """
BB = Board()
BB.BK2.move_piece(2, 7)
testlist.append(move_test(BB.BK2, 2, 7))  # 029 True
BB.BK2.move_piece(4, 8)
testlist.append(move_test(BB.BK2, 2, 7))  # 030 True
BB.BK2.move_piece(4, 6)
testlist.append(move_test(BB.BK2, 4, 6))  # 031 True
BB.BK2.move_piece(3, 4)
testlist.append(move_test(BB.BK2, 3, 4))  # 032 True
BB.BK2.move_piece(4, 2)
testlist.append(move_test(BB.BK2, 4, 2))  # 033 True
BB.BK2.move_piece(3, 4)
testlist.append(move_test(BB.BK2, 3, 4))  # 034 True
BB.BK2.move_piece(4, 6)
testlist.append(move_test(BB.BK2, 4, 6))  # 035 True
BB.BK2.move_piece(2, 7)
testlist.append(move_test(BB.BK2, 2, 7))  # 036 True
BB.BK2.move_piece(0, 6)
testlist.append(move_test(BB.BK2, 0, 6))  # 037 True
BB.BK2.move_piece(1, 4)
testlist.append(move_test(BB.BP4, 1, 4))  # 038 True
BB.WP7.move_piece(4, 7)
BB.WP7.move_piece(3, 7)
BB.WP7.move_piece(2, 7)
BB.BK2.move_piece(2, 7)
testlist.append(move_test(BB.BK2, 2, 7))  # 039 True

""" Testing rooks """
BB = Board()
BB.WR2.move_piece(6, 7)
testlist.append(move_test(BB.WP7, 6, 7))  # 040 True
BB.WR2.move_piece(5, 7)
testlist.append(not move_test(BB.WR2, 6, 7))  # 041 False
BB.WP7.move_piece(4, 7)
BB.WR2.move_piece(5, 7)
testlist.append(move_test(BB.WR2, 5, 7))  # 042 True
BB.WR2.move_piece(5, 2)
testlist.append(move_test(BB.WR2, 5, 2))  # 043 True
BB.WR2.move_piece(3, 2)
testlist.append(move_test(BB.WR2, 3, 2))  # 044 True
BB.WR2.move_piece(3, 7)
testlist.append(move_test(BB.WR2, 3, 7))  # 045 True
BB.WR2.move_piece(4, 7)
testlist.append(move_test(BB.WP7, 4, 7))  # 046 True
BB.WR2.move_piece(1, 7)
testlist.append(move_test(BB.WR2, 1, 7))  # 047 True
BB.WR2.move_piece(1, 8)
testlist.append(move_test(BB.WR2, 1, 7))  # 048 True

""" Testing bishops """
BB = Board()
BB.BB1.move_piece(1, 1)
testlist.append(move_test(BB.BP1, 1, 1))  # 049 True
BB.BB1.move_piece(2, 0)
testlist.append(not move_test(BB.BB1, 2, 0))  # 050 False
BB.BP1.move_piece(2, 1)
BB.BB1.move_piece(2, 0)
BB.legal_moves["B"][BB.BB1].items()
testlist.append(move_test(BB.BB1, 2, 0))  # 051 True
BB.BB1.move_piece(5, 3)
testlist.append(move_test(BB.BB1, 5, 3))  # 052 True
BB.BB1.move_piece(4, 4)
testlist.append(move_test(BB.BB1, 4, 4))  # 053 True
BB.BB1.move_piece(3, 3)
testlist.append(move_test(BB.BB1, 3, 3))  # 054 True
BB.BB1.move_piece(0, 0)
testlist.append(move_test(BB.BR1, 0, 0))  # 055 True
BB.BB1.move_piece(6, 6)
testlist.append(move_test(BB.BB1, 6, 6))  # 056 True

""" Testing queens """
BB = Board()
BB.WP3.move_piece(4, 3)
BB.WQn.move_piece(4, 3)
testlist.append(move_test(BB.WP3, 4, 3))  # 057 True
BB.WQn.move_piece(5, 3)
testlist.append(move_test(BB.WQn, 5, 3))  # 058 True
BB.WQn.move_piece(2, 6)
testlist.append(move_test(BB.WQn, 2, 6))  # 059 True
BB.WQn.move_piece(1, 5)
testlist.append(move_test(BB.WQn, 1, 5))  # 060 True
BB.WQn.move_piece(5, 1)
testlist.append(move_test(BB.WQn, 5, 1))  # 061 True
BB.WQn.move_piece(5, 4)
testlist.append(move_test(BB.WQn, 5, 4))  # 062 True
BB.WQn.move_piece(6, 4)
testlist.append(move_test(BB.WP4, 6, 4))  # 063 True
BB.WQn.move_piece(5, 3)
testlist.append(move_test(BB.WQn, 5, 3))  # 064 True
BB.WQn.move_piece(5, 2)
BB.WQn.move_piece(6, 3)
testlist.append(move_test(BB.WQn, 6, 3))  # 065 True
BB.WQn.move_piece(7, 3)
testlist.append(move_test(BB.WQn, 7, 3))  # 066 True
BB.WQn.move_piece(8, 3)
testlist.append(move_test(BB.WQn, 7, 3))  # 067 True


""" Testing kings """
BB = Board()
BB.BP4.move_piece(3, 4)
BB.BKi.move_piece(1, 4)
testlist.append(move_test(BB.BKi, 1, 4))  # 068 True
BB.BKi.move_piece(2, 5)
testlist.append(move_test(BB.BKi, 2, 5))  # 069 True
BB.BKi.move_piece(2, 6)
testlist.append(move_test(BB.BKi, 2, 6))  # 070 True
BB.BKi.move_piece(3, 5)
testlist.append(move_test(BB.BKi, 3, 5))  # 071 True
BB.BKi.move_piece(4, 4)
BB.BKi.move_piece(3, 3)
testlist.append(move_test(BB.BKi, 3, 3))  # 072 True
BB.BKi.move_piece(2, 4)
testlist.append(move_test(BB.BKi, 2, 4))  # 073 True
BB.BKi.move_piece(1, 4)
testlist.append(move_test(BB.BKi, 1, 4))  # 074 True
BB.BKi.move_piece(2, 4)
BB.BKi.move_piece(2, 3)
testlist.append(move_test(BB.BKi, 2, 3))  # 075 True

""" Castling """
BB = Board()
BB.WP4.move_piece(4, 4)
BB.WB2.move_piece(2, 0)
BB.WK2.move_piece(5, 7)
BB.WKi.move_piece(7, 6)
testlist.append(move_test(BB.WR2, 7, 5))  # 076 True

BB.BP4.move_piece(3, 4)
BB.BB2.move_piece(5, 0)
BB.BK2.move_piece(2, 7)
BB.BKi.move_piece(0, 6)
testlist.append(move_test(BB.BR2, 0, 5))  # 077 True

BB = Board()
BB.WP4.move_piece(4, 4)
BB.WP3.move_piece(4, 3)
BB.WQn.move_piece(6, 4)
BB.WK1.move_piece(5, 0)
BB.WB1.move_piece(6, 3)
BB.WKi.move_piece(7, 2)
testlist.append(move_test(BB.WR1, 7, 3))  # 078 True

BB.BP4.move_piece(3, 4)
BB.BP3.move_piece(3, 3)
BB.BQn.move_piece(1, 4)
BB.BK1.move_piece(2, 0)
BB.BB1.move_piece(1, 3)
BB.BKi.move_piece(0, 2)
BB.find_legal_moves()
testlist.append(move_test(BB.BR1, 0, 3))  # 079 True

BB = Board()
BB.WP4.move_piece(4, 4)
BB.WP3.move_piece(4, 3)
BB.WQn.move_piece(6, 4)
BB.WK1.move_piece(5, 0)
BB.WB1.move_piece(6, 3)
BB.WB1.move_piece(3, 0)
BB.BP3.move_piece(3, 3)
BB.WQn.move_piece(5, 4)
BB.BB1.move_piece(4, 6)
BB.WKi.move_piece(7, 2)
testlist.append(not move_test(BB.WR1, 7, 3))  # 080 False

BB.BP4.move_piece(3, 4)
BB.BQn.move_piece(1, 4)
BB.BK1.move_piece(2, 0)
BB.BP2.move_piece(3, 2)
BB.BKi.move_piece(0, 2)
BB.find_legal_moves()
testlist.append(not move_test(BB.BR1, 0, 3))  # 081 False

BB.WB2.move_piece(1, 0)
BB.WB1.move_piece(6, 3)
BB.BKi.move_piece(0, 2)
testlist.append(move_test(BB.BR1, 0, 3))  # 082 True
BB.WQn.move_piece(6, 4)
BB.WKi.move_piece(7, 2)
testlist.append(move_test(BB.WR1, 7, 3))  # 083 True

""" Testing kill piece """
testlist.append(BB.BR1.is_alive)  # 084 True
BB.kill_piece(BB.BR1.row, BB.BR1.column)
testlist.append(not BB.BR1.is_alive)  # 085 False

""" Testing reverseMove """
BB = Board()
BB.WK2.move_piece(6, 4)
testlist.append(move_test(BB.WP4, 6, 4))  # 086 True
BB.WP4.move_piece(4, 4)
BB.print_board()
BB.reverseMove(BB.WP4, 6, 4, 4, 4, "charge", 30, None)
BB.find_legal_moves()
BB.WB2.move_piece(6, 4)
testlist.append(move_test(BB.WP4, 6, 4))  # 087 True
BB.WP4.move_piece(4, 4)
BB.BP5.move_piece(3, 5)
BB.WP4.move_piece(3, 5)
BB.reverseMove(BB.WP4, 4, 4, 3, 5, "attack", 30, BB.BP5)
BB.find_legal_moves()
BB.BP5.move_piece(4, 5)
testlist.append(move_test(BB.BP5, 4, 5))  # 088 True
BB.WP4.move_piece(3, 4)
testlist.append(move_test(BB.WP4, 3, 4))  # 089 True

""" Performing tests """
run_tests(testlist)
