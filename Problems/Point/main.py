from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, to_point):
        return (sqrt((self.x - to_point.x) ** 2
                     + (self.y - to_point.y) ** 2))
