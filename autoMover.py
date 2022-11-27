import pyautogui
import time

class AutoMover:

    def __init__(self, x_top_left,y_top_left,square_size):
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.square_size = square_size
        #Colocamos primero el raton arriba izquierda
        pyautogui.moveTo(x_top_left + square_size/2, y_top_left + square_size/2 ,0.5)


    def moveToSquare(self,square_notation):
        
        time.sleep(1)

        letter2number = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        x = letter2number[square_notation[0:1]]
        y = 8 - int(square_notation[1:2]) 
        offset = self.square_size/2

        pyautogui.moveTo(self.x_top_left + x*self.square_size + offset,self.y_top_left + y*self.square_size + offset,0.5)


    def clickAndMoveTo(self,square_notation):
        letter2number = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        x = letter2number[square_notation[0:1]]
        y = 8 - int(square_notation[1:2]) 
        offset = self.square_size/2
        pyautogui.dragTo(self.x_top_left + x*self.square_size + offset,self.y_top_left + y*self.square_size + offset,button='left')

    def movePiece(self,starting_pos, ending_pos):
        self.moveToSquare(starting_pos)
        self.clickAndMoveTo(ending_pos)

mover = AutoMover(586,167,99)
mover.movePiece("c1","h6")
