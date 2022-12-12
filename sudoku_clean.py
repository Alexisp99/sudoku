import pandas as pd
import numpy as np
import random

################################################################################################################################
                                                       #Sudoku Checker#
################################################################################################################################

def verif_h_v(df):
    for i in range(9):
        return df[i].is_unique or df.iloc[i].is_unique

def check_block(i,j,df):
    liste = []
    for x in range(i,i+3):
        for y in range(j,j+3):
            liste.append(df[x][y])
    return len(set(liste)) == len(liste)  
