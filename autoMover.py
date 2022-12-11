import pyautogui
import time

class AutoMover:

    def __init__(self, x_top_left,y_top_left,square_size,color):
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.square_size = square_size
        self.color = color

        if color == 'w':
            self.letter2number = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        else:
            self.letter2number = {"h":0,"g":1,"f":2,"e":3,"d":4,"c":5,"b":6,"a":7}



    def moveToSquare(self,square_notation):
        x = self.letter2number[square_notation[0:1]]
        if self.color == 'w':
            y = 8 - int(square_notation[1:2])
            offsetx = self.square_size/2
            offsety = offsetx
        else:
            y = int(square_notation[1:2])
            offsetx = self.square_size/2
            offsety = -self.square_size/2
        

        pyautogui.moveTo(self.x_top_left + x*self.square_size + offsetx,self.y_top_left + y*self.square_size + offsety,0.5)


    def clickAndMoveTo(self,square_notation):
        x = self.letter2number[square_notation[0:1]]
        if self.color == 'w':
            y = 8 - int(square_notation[1:2])
            offsetx = self.square_size/2
            offsety = offsetx
        else:
            y = int(square_notation[1:2])
            offsetx = self.square_size/2
            offsety = -self.square_size/2
        offset = self.square_size/2
        pyautogui.dragTo(self.x_top_left + x*self.square_size + offset,self.y_top_left + y*self.square_size + offsety,button='left')

    def movePiece(self,starting_pos, ending_pos):
        self.moveToSquare(starting_pos)
        self.clickAndMoveTo(ending_pos)


