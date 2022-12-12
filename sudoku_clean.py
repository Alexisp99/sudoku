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

def sudoku_checker(df):
    if verif_h_v(df) != True:
        return "Grille non valide"

    for i in range(0,9,3):
        for j in range(0,9,3):
            if check_block(i,j,df) != True:
                return "Grille non valide"
    return "Grille valide"


################################################################################################################################
                                                       #Sudoku Solver#
################################################################################################################################

def sudoku_solver(df, creator = False):

    # initialisation de la condition de sortie
    global n
    n = 0
    df = check_entry_value(df)

    if replace_value(df, creator) == False and creator == False:
        print("Cette grille comporte plusieurs solutions")
    else :
        if creator == False:
            print("Cette grille est unique")


def replace_value(df, creator):
    global n
    n = 0
    #Condition de sortie
    if n > 1:
        return False

    #Parcours le tableau
    for i in range(0,9,3):
        for j in range(0,9,3):

            #Parcours le tableau par matrice de 3*3
            for x in range(i,i+3):
                for y in range(j,j+3):

                    # Si une case est vide, créer une liste des valeurs présente sur chaque ligne, colonne et block
                    if df[x][y] not in [1,2,3,4,5,6,7,8,9]:
                        liste = list(set(check_row(df,y) + check_col(df,x) + check_block(df,i,j)))

                        # Prend un nombre qui n'est pas dans la listes des valeurs présente
                        for i in nb_choice(liste):

                            df[x][y] = i


                            #Backtracking,si le nombre choisi bloque le prochain chemin, backtrack ici, et prend le nombre
                            #suivant de la liste.
                            #Si la liste est vide, passe à l'étape d'après
                            replace_value(df, creator)
                            df[x][y] = 0

                        #Si la liste est vide return False si le nombre de solution n > 1, sinon return True
                        if n > 1 :
                            return False
                        else :
                            return True

    #Affiche chaque solution et incrémente +1 n pour chaque solution trouvé
    if creator == False :
        print_sudoku(df)
    n+=1

def nb_choice(liste):
    #Retourne une liste de nombre qui ne sont pas dans la liste des nombre présent sur les lignes,colonnes, et bloc
    number = [1,2,3,4,5,6,7,8,9]
    liste_choice = []
    for i in number:
        if i not in liste :
            liste_choice.append(i)
    return liste_choice


def check_block(df,i,j):
    #Retourne une liste de nombre présent sur une matrice 3*3
    liste = []
    for x in range(i,i+3):
        for y in range(j,j+3):
            liste.append(df[x][y])
    return liste


def check_row(df,y):
    #Retourne une liste de nombre présent sur une ligne
    return list(df.loc[y])

def check_col(df,x):
    #Retourne une liste de nombre présent sur une colonne
    return list(df[x])

def check_entry_value(df):
    #convert the entry sudoku in dataframe
    #work with list, dataframe, array
    return pd.DataFrame(df)

def print_sudoku(board):
    print("- - - - - - - - - - - - - - - - -")
    for row in range(len(board)):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - - - - - - -")

        for col in range(len(board[0])):
            if col % 3 == 0 and col != 0 :
                print(" | ", end="")

            if col == 8:
                print(" " + str(board[row][col]))
            else:
                print(" " +str(board[row][col]) + " ", end="")
    print("- - - - - - - - - - - - - - - - -")
    print("\n")

################################################################################################################################
                                                       #Sudoku Creator#
################################################################################################################################

def grid() :
    grid = ([
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    ])

    return pd.DataFrame(grid)


def sudoku_creator():

    # initialisation de la condition de sortie
    global m
    m = 0
    replace_values(grid())

def replace_values(df):
    global m

    #Condition de sortie
    if check_full(df):
        m+=1
        remove_value(df)
        print_sudoku(df)
        return True

    #Parcours le tableau
    for i in range(0,9,3):
        for j in range(0,9,3):

            #Parcours le tableau par matrice de 3*3
            for x in range(i,i+3):
                for y in range(j,j+3):

                    # Si une case est vide, créer une liste des valeurs présente sur chaque ligne, colonne et block
                    if df[x][y] not in [i for i in range(1,10)]:
                        liste = list(set(check_row(df,y) + check_col(df,x) + check_block(df,i,j)))

                        # Prend un nombre qui n'est pas dans la listes des valeurs présente
                        for i in nb_choice(liste):

                            df[x][y] = i


                            #Backtracking,si le nombre choisi bloque le prochain chemin, backtrack ici, et prend le nombre
                            #suivant de la liste.
                            #Si la liste est vide, passe à l'étape d'après
                            replace_values(df)

                            df[x][y] = 0
                            if m > 0:
                                return True


                        #Si la liste est vide return False si le nombre de solution n > 1, sinon return True

                        return False

    #Affiche chaque solution et incrémente +1 n pour chaque solution trouvé

    return True

def check_full(df):
    count = 0
    for i in range(9):
        for j in range(9):
            if df[i][j] in [1,2,3,4,5,6,7,8,9]:
                count+=1
    if count == 81:
        return True

def remove_value(df):
    difficulty = pick_difficulty()
    nb_zero = 0
    if difficulty == "easy" :
        max_zero = 30
    elif difficulty == "medium":
        max_zero = 40
    elif difficulty == "hard":
        max_zero = 50
    else :
        max_zero = 10

    while nb_zero < max_zero :

        x = random.randint(0,8)
        y = random.randint(0,8)
        if df[x][y] != 0 :
            df[x][y] = 0
            nb_zero+=1
        if sudoku_solver(df,True) == False:
            random.shuffle(df)

def pick_difficulty():
    return input("choose difficulty : easy | medium | hard ")

################################################################################################################################
                                                 #Numpy Sudoku Checker#
################################################################################################################################

def numpy_check_row(arr,i):
    #check the length of the list of unique elements for each row
    return len(np.unique(arr[i])) == 9


def numpy_check_col(arr,i):
    #check the length of the list of unique elements for each col
    return len(np.unique(arr[:,i])) == 9

def numpy_check_block(arr,i):
    #check the length of the list of unique elements for each matrix 3*3
    return len(np.unique(arr[i//3+i//3*2 : i//3*3+3, i%3+i%3*2 : i%3*3+3])) == 9


def numpy_sudoku_checker(arr):
    #iterate in the 9 row, 9col and 9 matrix 3*3
    for i in range(9):
        if numpy_check_row(arr,i) != True or numpy_check_col(arr,i) != True or numpy_check_block(arr,i) != True:
             return print("Grille non valide")
    return print("Grille valide")

################################################################################################################################
                                                 #Numpy Sudoku Solver#
################################################################################################################################

def numpy_sudoku_solver(arr):
    # initialisation de la condition de sortie
    global n
    n = 0
    if numpy_replace_value(arr) == False:
        print("Cette grille comporte plusieurs solutions")
    else :
        print("Cette grille est unique")

def numpy_replace_value(arr):
    global n

    #Condition de sortie
    if n > 1:
        return False

    #find zero in array
    result = np.where(arr == 0)
    list_coordinates= list(zip(result[0], result[1]))

    for coordinate in list_coordinates:
        for number in range(1,10):
            if check_blocks(arr,number,coordinate) == False and check_rows(arr,number,coordinate) == False and check_cols(arr,number,coordinate) == False:
                arr[coordinate] = number

                if np.count_nonzero(arr) == 81 :
                    n+=1
                    print_sudoku(arr)

                #Backtracking,si le nombre choisi bloque le prochain chemin, backtrack ici, et prend le nombre
                #suivant de la liste.
                #Si la liste est vide, passe à l'étape d'après
                numpy_replace_value(arr)

                arr[coordinate] = 0

            #Si la liste est vide return False si le nombre de solution n > 1, sinon return True
        return False if n > 1 else True

def check_blocks(arr,number,coordinate):
    #Retourne Truesi le nombre est présent sur une matrice 3*3
    x = coordinate[0]
    y = coordinate[1]
    return number in arr[x//3+x//3*2 : x//3*3+3, y//3+y//3*2 : y//3*3+3]

def check_rows(arr,number,coordinate):
    #Retourne True si le nombre est présent sur une ligne
    x = coordinate[0]
    return number in arr[x]

def check_cols(arr, number,coordinate):
    #Retourne True si le nombre est présent sur une colonne
    y = coordinate[1]
    return number in arr[:,y]

################################################################################################################################
                                     #Sudoku Solver without verify unique solution#
################################################################################################################################

def not_unique_sudoku_solver(arr):

    #find zero
    result = np.where(arr == 0)
    list_coordinates= list(zip(result[0], result[1]))

    for coordinate in list_coordinates:
        for number in range(1,10):
            if checks_blocks(arr,number,coordinate) == False and checks_rows(arr,number,coordinate) == False and checks_cols(arr,number,coordinate) == False:
                arr[coordinate] = number

                #Backtracking,si le nombre choisi bloque le prochain chemin, backtrack ici, et prend le nombre
                #suivant de la liste.
                #Si la liste est vide, passe à l'étape d'après
                if not_unique_sudoku_solver(arr) == True:
                    return True

                arr[coordinate] = 0

        #Si la liste est vide return False
        return False

    #return True une fois que notre liste de coordonnée est vide
    print_sudoku(arr)
    return True

def checks_blocks(arr,number,coordinate):
    #Retourne True si le nombre est présent sur une matrice 3*3
    x = coordinate[0]
    y = coordinate[1]
    return number in arr[x//3+x//3*2 : x//3*3+3, y//3+y//3*2 : y//3*3+3]

def checks_rows(arr,number,coordinate):
    #Retourne True si le nombre est présent sur une ligne
    x = coordinate[0]
    return number in arr[x]

def checks_cols(arr, number,coordinate):
    #Retourne True si le nombre est présent sur une colonne
    y = coordinate[1]
    return number in arr[:,y]

################################################################################################################################
                                     #Sudoku Creator without verify unique solution#
################################################################################################################################

def grid() :
    grid = ([
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", "."],
    ])

    return pd.DataFrame(grid)


def not_unique_sudoku_creator():

    # initialisation de la condition de sortie
    global m
    m = 0
    not_unique_replace_values(grid())

def not_unique_replace_values(df):
    global m

    #Condition de sortie
    if check_full(df):
        m+=1
        remove_value(df)
        print_sudoku(df)
        return True

    #Parcours le tableau
    for i in range(0,9,3):
        for j in range(0,9,3):

            #Parcours le tableau par matrice de 3*3
            for x in range(i,i+3):
                for y in range(j,j+3):

                    # Si une case est vide, créer une liste des valeurs présente sur chaque ligne, colonne et block
                    if df[x][y] not in [i for i in range(1,10)]:
                        liste = list(set(check_row(df,y) + check_col(df,x) + check_block(df,i,j)))

                        # Prend un nombre qui n'est pas dans la listes des valeurs présente
                        for i in nb_choice(liste):

                            df[x][y] = i


                            #Backtracking,si le nombre choisi bloque le prochain chemin, backtrack ici, et prend le nombre
                            #suivant de la liste.
                            #Si la liste est vide, passe à l'étape d'après
                            not_unique_replace_values(df)

                            df[x][y] = 0
                            if m > 0:
                                return True


                        #Si la liste est vide return False si le nombre de solution n > 1, sinon return True

                        return False

    #Affiche chaque solution et incrémente +1 n pour chaque solution trouvé

    return True

def check_full(df):
    count = 0
    for i in range(9):
        for j in range(9):
            if df[i][j] in [1,2,3,4,5,6,7,8,9]:
                count+=1
    if count == 81:
        return True

def remove_value(df):
    difficulty = pick_difficulty()
    nb_zero = 0
    if difficulty == "easy" :
        max_zero = 30
    elif difficulty == "medium":
        max_zero = 40
    elif difficulty == "hard":
        max_zero = 50
    else :
        max_zero = 10

    while nb_zero < max_zero :

        x = random.randint(0,8)
        y = random.randint(0,8)
        if df[x][y] != 0 :
            df[x][y] = 0
            nb_zero+=1
        if replace_value(df,True) == False:
            random.shuffle(df)

def pick_difficulty():
    return input("choose difficulty : easy | medium | hard ")
