class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        if self.c ** 2 == self.a ** 2 + self.b ** 2:
            self.S = leg_1 * leg_2 / 2
        else:
            self.S = "Not right"


# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

triangle = RightTriangle(input_c, input_a, input_b)
print(triangle.S)
