
from individual import Individual
from random import randint

class Population():
    def __init__(self, initial_size, src_image, width, height):
        self.src_image = src_image
        self.width = width
        self.height = height
        self.individuals = []
        # Create the initial population with random dna
        for i in range(initial_size):
            individual = Individual(src_image, width, height)
            individual.randomDna()
            self.individuals.append(individual)

    def calcFitness(self):
        for individual in self.individuals:
            individual.calcFitness()

    def getOld(self):
        i = 0
        for individual in self.individuals:
            individual.lifetime -= 1
            # If no lifetime left, individual is dead
            if (individual.lifetime <= 0):
                del self.individuals[i]
            i += 1

    def makeBabys(self, number):
        # Find the sum of all fitness on the current population
        fitness_sum = 0
        for individual in self.individuals:
            fitness = individual.fitness
            if fitness is None:
                raise NameError("Trying to make babys before running fitness test")
            fitness_sum += fitness
        # Get number babys
        for i in range(number):
            # Find a mum
            target_fit = randint(0, fitness_sum - 1)
            current_fit = 0
            i = 0
            while (current_fit < target_fit):
                current_fit += self.individuals[i].fitness
                i += 1
            i -= 1
            mum = self.individuals[i]
            # Find a dad
            target_fit = randint(0, fitness_sum - 1)
            current_fit = 0
            i = 0
            while (current_fit < target_fit):
                current_fit += self.individuals[i].fitness
                i += 1
            i -= 1
            dad = self.individuals[i]
            # Get the baby
            baby = mum.makeBaby(dad)
            # Add it to the population
            self.individuals.append(baby)

    def getBestIndividual(self):
        best_fitness = 0
        best_individual = None
        for individual in self.individuals:
            if (individual.fitness is not None and
                individual.fitness > best_fitness):
                best_fitness = individual.fitness
                best_individual = individual
        return best_individual

    def size(self):
        return (len(self.individuals))

    def averageFitness(self):
        total = 0
        for individual in self.individuals:
            total += individual.fitness
        return (total / len(self.individuals))
                
