from math import floor
from random import randint, random, choice
import string
import matplotlib.pyplot as plt


def comp(elem1, elem2):
    assert len(elem1) == len(elem2)
    for i in range(len(elem1)):
        if elem1[i] != elem2[i]:
            return False
    return True


def fitnesscat(elem):
    # word = ['s', 'u', 'p', 'e', 'r', 'p','a','l','a','b','r','a']
    word = ['c', 'a', 't']
    fitting = 0
    assert len(elem) == len(word)
    for i in range(len(word)):
        if elem[i] == word[i]:
            fitting = fitting + 1
    return fitting


def fitness12(elem):
    # word = ['s', 'u', 'p', 'e', 'r', 'p','a','l','a','b','r','a']
    word = ['c', 'a', 't']
    fitting = 0
    assert len(elem) == len(word)
    for i in range(len(word)):
        if elem[i] == word[i]:
            fitting = fitting + 1
    return fitting


def fitness(elem):
    # word = ['s', 'u', 'p', 'e', 'r', 'p','a','l','a','b','r','a','c','o','o','l']
    word = ['c', 'a', 't']
    fitting = 0
    assert len(elem) == len(word)
    for i in range(len(word)):
        if elem[i] == word[i]:
            fitting = fitting + 1
    return fitting


def fitness(elem):
    # word = ['s', 'u', 'p', 'e', 'r', 'p','a','l','a','b','r','a']
    word = ['c', 'a', 't']
    fitting = 0
    assert len(elem) == len(word)
    for i in range(len(word)):
        if elem[i] == word[i]:
            fitting = fitting + 1
    return fitting


def fitnessNum(elem):
    # word = ['s', 'u', 'p', 'e', 'r', 'p','a','l','a','b','r','a']
    word = [1, 0, 1, 0, 0, 1, 1, 0, 0, 0]
    #word = [1, 0, 1, 0]
    fitting = 0
    assert len(elem) == len(word)
    for i in range(len(word)):
        if elem[i] == word[i]:
            fitting = fitting + 1
    return fitting


def gen(elem):
    return randint(0, 1)


def genstr(elem):
    return choice(string.ascii_lowercase)


def genqueen(n):
    return randint(0, n - 1)


def queenfitness(elem):
    ngenes = len(elem)
    # Verificar choces en las columnas
    duplicated_exc = set(elem)
    fitness = len(duplicated_exc)
    col_up = False
    col_down = False
    # Verificar choques en las diagonales
    for i in range(ngenes - 1):
        gene = elem[i]
        for j in range(1, ngenes - i):
            next = elem[i + j]
            if next == gene + j:
                col_up = True
            elif next == gene - j:
                col_down = True
        if col_up == True:
            fitness -= 1
        if col_down == True:
            fitness -= 1
    return fitness


class GeneticAlgorithm:
    def __init__(self, ngens, npopulation, fitness, gen, mutationRate, tolerancy=10):
        self.ngens = ngens
        self.npopulation = npopulation
        self.population = []
        self.fit = []
        self.fitness = fitness
        self.gen = gen
        self.mutationRate = mutationRate
        self.tolerancy = tolerancy
        self.bestfit = []
        self.generation = []

    def getGenerations(self):
        return self.generation

    def getFitness(self):
        return self.bestfit

    # Step 1
    def initPopulation(self):
        for i in range(self.npopulation):
            element = []
            for j in range(self.ngens):
                element.append(self.gen(self.ngens))
            self.population.append(element)

    # Step 2

    def checkfitness(self):
        self.fit = []
        for elem in self.population:
            self.fit.append(self.fitness(elem))

    # Step 3: Tournament Selection
    def tournament_selection(self, k):
        best = None
        if k == 0:
            best = 0
        for i in range(0, k):
            ind = randint(0, k)
            if (best == None) or (self.fit[ind] > self.fit[best]):
                best = ind
        return best

    # Step4: Reproduction. Each baby must be created with cross over
    # and mutation
    def reproduction(self):
        nparents = 2 * len(self.population)
        parents = []
        babies = []
        k = floor(3 * len(self.population) / 4)
        # elejir a los padres
        for i in range(0, 2 * nparents):
            # Shuffle artesanal
            for index in range(len(self.population)):
                a = randint(0, len(self.population) - 1)
                b = randint(0, len(self.population) - 1)
                self.population[a], self.population[b] = self.population[b], self.population[a]
                self.fit[a], self.fit[b] = self.fit[b], self.fit[a]

            best = self.tournament_selection(k)
            parents.append(self.population[best])

        # Crear a los hijos
        for i in range(0, len(self.population) * 2, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            mixingPoint = randint(0, self.ngens)
            baby = []

            for j in range(0, self.ngens):
                # Cross Over
                if j < mixingPoint:
                    baby.append(parent1[j])
                else:
                    baby.append(parent2[j])
                # Mutation
                for k in range(len(baby)):
                    if random() < self.mutationRate:
                        baby[k] = self.gen(self.ngens)
            babies.append(baby)
            self.population = babies

    def getBestIndex(self):
        best = 0
        assert len(self.population) == len(self.fit)
        for i in range(len(self.fit)):
            if self.fit[i] > self.fit[best]:
                best = i
        return best

    def run(self):
        # paso1
        self.initPopulation()
        self.checkfitness()
        index = self.getBestIndex()
        guess = self.population[index]
        guessFitness = self.fit[index]

        last = []
        last.append(guess)
        self.end = 0
        iter = 1


        while self.ngens > guessFitness:

            if self.end:
                break
            self.generation.append(iter)
            print("Generation", format(iter), ";Current best:", format(guess))
            self.reproduction()
            self.checkfitness()
            guess = self.population[self.getBestIndex()]
            guessFitness = self.fit[self.getBestIndex()]
            self.bestfit.append(guessFitness)
            if len(last) < self.tolerancy:
                last.append(guess)
            else:
                last.pop(0)
                last.append(guess)
                if comp(last[0], guess):
                    for elem in last[1:]:
                        if not comp(elem, guess):
                            self.end = 0
                            break
                        else:
                            self.end = 1
                            continue

            iter = iter + 1

        print("best: ", guess)

        return guess


class Metrics:
    def fitnesscurve(self, ngene, npob, fitnessfunc, genfunc, mr, tol):
        ga = GeneticAlgorithm(ngene, npob, fitnessfunc, genfunc, mr, tol)
        ga.run()
        print("generaciones:", ga.getGenerations())
        print("fitness", ga.getFitness())
        plt.plot(ga.getGenerations(), ga.getFitness())
        plt.ylabel("Fitness")
        plt.xlabel("Generación")
        plt.title("Curva de fitness")
        plt.show()

    def averagegenscurve(self, ngene, npob, fitnessfunc, genfunc, mr, tol):
        random.setseed(25)

    # GeneticAlgorithm(100, 100, queenfitness, genqueen, 0.01, 1).run()


Metrics().fitnesscurve(3, 100, fitness, genstr, 0.01, 10)
