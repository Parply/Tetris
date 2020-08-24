"""
Using code from https://github.com/omgimanerd/tetris-bot/
"""

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

class Field():
    WIDTH = 10
    HEIGHT = 22
    
    def __init__(self, state=None):
        if state:
            self.state = state
        else:
            self.state = [[' ' for cols in range(Field.WIDTH)]
                          for rows in range(Field.HEIGHT)]

    def __str__(self):
        BAR = '   ' + '-' * (Field.WIDTH * 2 + 1) + '\n    ' + \
            ' '.join(map(str, range(Field.WIDTH))) + '\n'
        return BAR + '\n'.join([
            '{:2d} |'.format(i) + ' '.join(row) + '|'
                for i, row in enumerate(self.state)]) + '\n' + BAR
    def _test_tetromino(self, tetromino, row, column):
        """
        Tests to see if a tetromino can be placed at the specified row and
        column. It performs the test with the bottom left corner of the
        tetromino at the specified row and column.
        """
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        assert row < Field.HEIGHT
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                if tetromino[ti][tj] != ' ' and self.state[si][sj] != ' ':
                    return False
        return True         

    def _place_tetromino(self, tetromino, row, column):
        """
        Place a tetromino at the specified row and column.
        The bottom left corner of the tetromino will be placed at the specified
        row and column. This function does not perform checks and will overwrite
        filled spaces in the field.
        """
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        assert row - tetromino.height() + 1 >= 0
        assert row < Field.HEIGHT
        for ti, si in list(enumerate(range(row - tetromino.height() + 1,
                                           row + 1)))[::-1]:
            for tj, sj in enumerate(range(column, column + tetromino.width())):
                if tetromino[ti][tj] != ' ':
                    self.state[si][sj] = tetromino[ti][tj]

    def _get_tetromino_drop_row(self, tetromino, column):
        """
        Given a tetromino and a column, return the row that the tetromino
        would end up in if it were dropped in that column.
        Assumes the leftmost column of the tetromino will be aligned with the
        specified column.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        last_fit = -1
        for row in range(tetromino.height(), Field.HEIGHT):
            if self._test_tetromino(tetromino, row, column):
                last_fit = row
            else:
                return last_fit
        return last_fit

    def _line_clear(self):
        """
        Checks and removes all filled lines.
        """
        self.state = list(filter(lambda row: row.count(' ') != 0, self.state))
        while len(self.state) < Field.HEIGHT:
            self.state.insert(0, [' ' for col in range(Field.WIDTH)])

    def copy(self):
        """
        Returns a shallow copy of the field.
        """
        return Field([row[:] for row in self.state])

    def drop(self, tetromino, column):
        """
        Drops a tetromino in the specified column.
        The leftmost column of the tetromino will be aligned with the specified
        column.
        Returns the row it was dropped in for computations.
        """
        assert isinstance(tetromino, Tetromino)
        assert column >= 0
        assert column + tetromino.width() <= Field.WIDTH
        row = self._get_tetromino_drop_row(tetromino, column)
        assert row != -1
        self._place_tetromino(tetromino, row, column)
        self._line_clear()
        return row

    def count_gaps(self):
        """
        Check each column one by one to make sure there are no gaps in the
        column.
        """
        return sum(
            ["".join([row[col] for row in self.state]).lstrip().count(' ')
             for col in range(Field.WIDTH)])

    def height(self):
        """
        Returns the height on the field of the highest placed tetromino on the
        field.
        """
        for i, row in enumerate(self.state):
            if ''.join(row).strip():
                return Field.HEIGHT - i

