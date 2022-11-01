import os
from chess import Chess
import numpy as np
import cv2 as cv
from ChessBoardDetection import ChessBoardAnalizer
import warnings
import time

warnings.filterwarnings("ignore")

directory = './test_images'

#test_image, laptop_board
standard_list = [
    "./test_images\\laptop_board.png", "./test_images\\test_image.png"
]
standard_conf = [
    -4, -2, -3, -5, -6, -3, -2, -4, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 4, 2, 3, 5, 6, 3, 2, 4
]

#test_board,test_board_4,test_board_5,test_board_6,test_board_7,test_board_8,test_board_9
test_conf_1_list = [
    "./test_images\\test_board.png", "./test_images\\test_board_4.png",
    "./test_images\\test_board_5.png", "./test_images\\test_board_6.png",
    "./test_images\\test_board_7.png", "./test_images\\test_board_8.png",
    "./test_images\\test_board_9.png"
]
test_conf_1 = [
    -4, 0, 0, -6, 0, 0, 0, -4,
    -1, -1, -1, 0, 0, -1, -1, 0,
    0, 0, 0, 0, -1, -2, 0, -1,
    0, 0, -3, 0, 0, -3, 0, 0,
    3, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 0, -1, 0, 0, 0, 0,
    1, 1, 1, 1, 0, 0, 1, 1,
    4, 2, 3, 0, 6, 0, 0, 4
]

#test_board_3
test_conf_2_list = ["./test_images\\test_board_3.png"]
test_conf_2 = [
    -4, 0, 0, -6, 0, 0, 0, -4,
    -1, -1, -1, 0, 0, -1, -1, 0,
    0, 0, 0, 0, -1, -2, 0, -1,
    0, 0, -3, 0, 0, -3, 0, 0,
    3, 0, 0, 0, -1, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    1, 1, 1, 1, 5, 0, 1, 1,
    4, 2, 3, 0, 6, 0, 0, 4
]

#test_board_1, test_board_2
test_conf_3_list = ["./test_images\\test_board_1.png","./test_images\\test_board_2.png"]
test_conf_3 = [
    -4, 0, 0, 0, 0, 0, -4, 0,
    -1, 0, -6, 0, 0, -1, -1, 0,
    0, 0, -1, 0, 0, -2, 0, -1,
    0, 0, -3, -1, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    1, 1, 0, 1, 0, 0, 0, 1,
    4, 0, 3, 0, 6, -3, 0, 0
]

test_conf_4_list = ["./test_images\\test_board_1.png","./test_images\\test_board_10.png"]
test_conf_4 = [
    0, -2, -3, 2, 0, 0, 0, -4,
    0, 0, -1, -1, -3, 0, 0, -1,
    -4, 0, 0, 0, 0, -6,-1, -2,
    0, -1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 1, 1, 0, 0, 1, 3,
    1, 0, 0, 0, 1, 0, 0, 1,
    4, 0, 3, 5, 0, 4, 6, 0
]

def testImageToChess(filename):

    print("\tTesting ", filename, end='')

    tablero = cv.imread(filename, cv.IMREAD_UNCHANGED)
    chessBoardAnalizer = ChessBoardAnalizer(tablero)
    resulting_board = chessBoardAnalizer.processBoard()

    if filename in standard_list:
        if np.allclose(resulting_board.getInnerMatrix(),
                       np.reshape(standard_conf, (8, 8))):
            print(" ----> Correct!")
        else:
            print(" ----> INCORRECT")
    elif filename in test_conf_1_list:
        if np.allclose(resulting_board.getInnerMatrix(),
                       np.reshape(test_conf_1, (8, 8))):
            print(" ----> Correct!")
        else:
            print(" ----> INCORRECT")
    elif filename in test_conf_2_list:
        if np.allclose(resulting_board.getInnerMatrix(),
                       np.reshape(test_conf_2, (8, 8))):
            print(" ----> Correct!")
        else:
            print(" ----> INCORRECT")
    elif filename in test_conf_3_list:
        if np.allclose(resulting_board.getInnerMatrix(),
                       np.reshape(test_conf_3, (8, 8))):
            print(" ----> Correct!")
        else:
            print(" ----> INCORRECT")
    elif filename in test_conf_4_list:
        if np.allclose(resulting_board.getInnerMatrix(),
                       np.reshape(test_conf_4, (8, 8))):
            print(" ----> Correct!")
        else:
            print(" ----> INCORRECT")

def calculateAvgExecutionTime():
    print("Calculating average execution time...")
    n_files = 4
    iteration = 0
    total_time = 0

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            iteration += 1
            if(iteration > n_files): break
            st1 = time.time()
            tablero = cv.imread(f, cv.IMREAD_UNCHANGED)
            chessBoardAnalizer = ChessBoardAnalizer(tablero)
            chessBoardAnalizer.processBoard()
            et1 = time.time()
            total_time += et1-st1

    print("\tAveragage execution time: ", total_time/4 , "seconds")
    

print("Running tests...")

st = time.time()

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        testImageToChess(f)


calculateAvgExecutionTime()

et = time.time()

print("")
print("\t\tTime employed in execution: ", et-st, " seconds")