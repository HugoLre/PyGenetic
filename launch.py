#!/usr/bin/python3

from PIL import Image
import sys
import os
import shutil
import matplotlib.pyplot as plt
from population import Population
from time import time

if (len(sys.argv) != 2):
    print("Usage: " + sys.argv[0] + " <image to recreate>")
    exit()

# Open image to copy
src_image = Image.open(sys.argv[1])
image_width, image_height = src_image.size

# Create base population
pop = Population(100, src_image.convert("RGB"), image_width, image_height)

# Clean evolution directory
for f in os.listdir("evolution"):
    path = os.path.join("evolution/", f)
    os.remove(path)

# Infinite evole loop
x = []
avg_fit = []
i = 0
save_time = time()
print_time = time()
ctime = time()
while (True):
    disp = '\n' * 5
    disp += "#%d\n" % i
    disp += "Population size is %d\n" % pop.size()
    pop.calcFitness()
    average = pop.averageFitness()
    pop.makeBabys(50)
    best = pop.getBestIndividual()
    disp += "Best fitness is %d\n" % best.fitness
    disp += "Average fitness is %d\n" % average
    avg_fit.append(average)
    x.append(i)
    pop.getOld()
    if (i % 5 == 0):
        ctime = time()
    if (ctime > save_time + 120):
        # Write evolution every 10 seconds
        save_time = ctime
        best.saveAs("best.png")
        shutil.copy("best.png", "evolution/%d.png" % best.fitness)
        plt.plot(x, avg_fit, "red")
        plt.xlabel("tick")
        plt.ylabel("avg fitness")
        plt.savefig("evolve.png")
    if (ctime > print_time + 1):
        print_time = ctime
        # Print every second
        print(disp)
    i += 1
    
