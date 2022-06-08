# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 20:26:45 2016

@author: Philip
"""

from SkakMat2 import *
import time

B = Board()

B.WP4.move_piece(4, 4)
time.sleep(1)
B.BP2.move_piece(2, 2)
time.sleep(1)

B.WP3.move_piece(4, 3)
time.sleep(1)
B.BP3.move_piece(3, 3)
time.sleep(1)

B.WK1.move_piece(5, 2)
time.sleep(1)
B.BP3.move_piece(4, 4)
time.sleep(1)

B.WK1.move_piece(4, 4)
time.sleep(1)
B.BK1.move_piece(1, 3)
time.sleep(1)

B.WK1.move_piece(3, 6)
time.sleep(1)
B.BK2.move_piece(2, 5)
time.sleep(1)

B.WB2.move_piece(5, 3)
time.sleep(1)
B.BP4.move_piece(2, 4)
time.sleep(1)

B.WK2.move_piece(5, 5)
time.sleep(1)
B.BP7.move_piece(2, 7)
time.sleep(1)

B.WK1.move_piece(2, 4)
time.sleep(1)
B.BQn.move_piece(1, 4)
time.sleep(1)

B.WKi.move_piece(7, 6)
time.sleep(1)
B.BP5.move_piece(2, 4)
time.sleep(1)

B.WB2.move_piece(2, 6)
time.sleep(1)
B.BKi.move_piece(0, 3)
time.sleep(1)

B.WB1.move_piece(4, 5)
time.sleep(1)
B.BP1.move_piece(3, 1)
time.sleep(1)

B.WP0.move_piece(4, 0)
time.sleep(1)
B.BB1.move_piece(1, 1)
time.sleep(1)

B.WR2.move_piece(7, 4)
time.sleep(1)
B.BK2.move_piece(3, 3)
time.sleep(1)

B.WB1.move_piece(5, 6)
time.sleep(1)
B.BKi.move_piece(0, 2)
time.sleep(1)

B.WP0.move_piece(3, 1)
time.sleep(1)
B.BP2.move_piece(3, 1)
time.sleep(1)

B.WQn.move_piece(5, 3)
time.sleep(1)
B.BB1.move_piece(2, 2)
time.sleep(1)

B.WB2.move_piece(3, 5)
time.sleep(1)
B.BP5.move_piece(3, 5)
time.sleep(1)

B.WR2.move_piece(1, 4)
time.sleep(1)
B.BB2.move_piece(1, 4)
time.sleep(1)

B.WP2.move_piece(4, 2)
time.sleep(10)
""" Kasparov topples black king here """
""" Alternate ending """
B.BP2.move_piece(4, 2)
time.sleep(1)

B.WQn.move_piece(4, 2)
time.sleep(1)
B.BK2.move_piece(4, 1)
time.sleep(1)

B.WR1.move_piece(7, 4)
time.sleep(1)
B.BKi.move_piece(0, 3)
time.sleep(1)

B.WR1.move_piece(1, 4)
time.sleep(1)
B.BKi.move_piece(1, 4)
time.sleep(1)

B.WQn.move_piece(4, 1)
""" Now even wiki gives up """
