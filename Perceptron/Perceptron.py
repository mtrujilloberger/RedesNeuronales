from random import random, uniform


class Perceptron:
    def __init__(self, *, pesos=None, b=None, num=None):
        self.pesos = []
        if num == None:
            self.pesos = pesos
            self.b = b
        else:
            for i in range(0, num ):
                self.pesos.append(uniform(-2, 2))
            self.b = random()

    def feed(self, inputs):
        assert len(self.pesos) == len(inputs)
        equation = 0
        for i in range(0, len(inputs)):
            equation += inputs[i] * self.pesos[i]
        equation = equation + self.b
        return equation > 0

    def training(self, inputs, output):
        realOutput = self.feed(inputs)
        diff = output - realOutput
        lr = 0.1
        for i in range(0, len(inputs)):
            self.pesos[i] += (lr * inputs[i] * diff)
        self.b += (lr * diff)


class And(Perceptron):
    def __init__(self):
        super().__init__(pesos=[1, 1], b=-1.5)


class Or(Perceptron):
    def __init__(self):
        super().__init__(pesos=[1, 1], b=-0.5)


class NanD(Perceptron):
    def __init__(self):
        super().__init__(pesos=[-2, -2], b=3)


class Sum:
    def __init__(self):
        self.NanD1 = NanD()

    def feed(self, x1, x2):
        uno = self.NanD1.feed([x1, x2])
        dos = self.NanD1.feed([x1, uno])
        tres = self.NanD1.feed([x2, uno])
        sum = self.NanD1.feed([dos, tres])
        carry = self.NanD1.feed([uno, uno])
        return sum, carry


if __name__ == "__main__":
    suma = Sum()
    print(suma.feed(1, 1))
