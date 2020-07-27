import numpy as np

class shapes():
    TYPES = ['o','i','s','z','l','j','t']
    def __init__(self,state=None):
        self.state = state
        if self.state is None:
            self.state = TYPES[np.random.randint(0,len(TYPES))]
        self.shape=self.create(self.state)
    @staticmethod
    def otype():
        return [['O','O'],['O','O']]
    @staticmethod
    def itype():
        return [['I','I','I','I']]
    @staticmethod
    def stype():
        return [[' ','S','S'],['S','S',' ']]
    @staticmethod 
    def ztype():
        return [['Z','Z',' '],[' ','Z','Z']]
    @staticmethod
    def ltype():
        return [['L','L','L'],['L',' ',' ']]
    @staticmethod
    def jtype():
        return [['J','J','J'],[' ',' ','J']]
    @staticmethod
    def ttype():
        return [['T','T','T'],[' ','T',' ']]
    @staticmethod
    def create(type):
        return getattr(shapes, f"{type}type")()
    def height(self):
        return len(self.shape)
    def width(self):
        return len(self.shape[0])
    def rotate_right(self):
        self.shape = list(zip(*self.shape[::-1]))
    def rotate_left(self):
        self.shape = list(reversed(list(zip(*self.shape))))
    def flip(self):
        self.shape = [row[::-1] for row in self.shape[::-1]]
    def rotate(self,change):
        change = (change % 4)
        if change == 0:
            pass
        elif change == 1:
            self.rotate_right()
        elif change == 2:
            self.flip()
        elif change == 3:
            self.rotate_left()




