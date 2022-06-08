# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 18:52:03 2016

@author: Philip
"""

#!/usr/bin/python
import AI_v2
import SkakMat2 as SM
import multiprocessing as mp
import os
import copy

# class BentProcess (mp.process):
#
#    def setup(self, processID, pieceName, isWhite, branchBest, nRep,AI):
#        self.processID = processID
#        self.name = pieceName
#        self.isWhite = isWhite
#        self.branchBest = branchBest
#        self.nRep = nRep
#        self.AI = copy.deepcopy(AI)
#
#
#    def run(self):
#        self.info(self.processID + " " + self.pieceName)
#        #self.AI.bestMove(self.isWhite, self.branchBest, self.nRep)
#        return 0


def info(title):
    print(title)
    print("module name:", __name__)
    print("parent process:", os.getppid())
    print("process id:", os.getpid())


if __name__ == "__main__":
    pp = mp.Process(target=info, args="Hello")
    pp.start()
    pp.join()
