
from random import randint
from PIL import Image, ImageDraw

dna_len = 100
square_size_max_ratio = 4
square_size_min_ratio = 20
lifetime = 15
nb_sample = 200
mutation_per_baby = 1

# DNA = [ [x, y, size, r, g, b]  * dna_len]

class Individual():
    def __init__(self, src_image, width, height):
        self.dna = None
        self.fitness = None
        self.src_image = src_image
        self.width = width
        self.height = height
        self.max_fitness = nb_sample * 255 * 3
        self.lifetime = lifetime
        
    def setDna(self, dna):
        if (len(dna) != dna_len):
            raise NameError("DNA length is incorrect")
        self.dna = dna

    def randomDna(self):
        dna = []
        for i in range(dna_len):
            # Random parameters
            x = randint(0, self.width)
            y = randint(0, self.height)
            size = randint(self.width / square_size_min_ratio, self.width / square_size_max_ratio)
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            new = [x, y, size, r, g, b]
            dna.append(new)
        self.dna = dna

    def drawDna(self):
        # Draw an image from the instructions in the dna
        self.image = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(self.image)
        for form in self.dna:
            size = form[2]
            x_beg = form[0]
            x_end = x_beg + size
            y_beg = form[1]
            y_end = y_beg + size
            color = (form[3], form[4], form[5])
            draw.rectangle([x_beg, y_beg, x_end, y_end], fill=color, outline=color)
        del draw
        
    def calcFitness(self):
        if self.dna is None:
            raise NameError("Try to calculate fitness with empty dna")
        # Do not re-calculate the fitness: huge time gain
        if self.fitness is not None:
            return
        # Draw the image from dna
        self.drawDna()
        # For some sample pixel , compare the two images
        fitness = self.max_fitness
        for i in range(nb_sample):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            src_pix = self.src_image.getpixel((x, y))
            new_pix = self.image.getpixel((x, y))
            # Error is the difference in each primary color of the 2 pixels
            error = abs(src_pix[0] - new_pix[0])
            error += abs(src_pix[1] - new_pix[1])
            error += abs(src_pix[2] - new_pix[2])
            fitness -= error
        # Ampliy the fitness with pow, this formula is totaly arbitrary (but seem to work) !!
        self.fitness = int(pow((fitness / self.max_fitness * 2), 30))


    def makeBaby(self, dad):
        # print("Dad %d   Mum %d" % (dad.fitness, self.fitness))
        baby_dna = []
        # Random index to cut the dna at
        cut = randint(0, len(self.dna) - 1)
        # The beginning of the baby dna is our dna
        for i in range(cut):
            baby_dna.append(self.dna[i])
        # The end of the baby dna is it's dad dna
        for i in range(cut, len(self.dna)):
            baby_dna.append(dad.dna[i])
        # Apply some random mutation
        len_dna = len(baby_dna)
        for i in range(len_dna):
            # Probability to have a mutation on each form of the baby dna
            rand = randint(0, int(len_dna / mutation_per_baby))
            if (rand == 0):
                # Mutation, randomize !
                x = randint(0, self.width)
                y = randint(0, self.height)
                size = randint(self.width / square_size_min_ratio, self.width / square_size_max_ratio)
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                baby_dna[i] = [x, y, size, r, g, b]
        # Create and return the baby
        baby = Individual(self.src_image, self.width, self.height)
        baby.setDna(baby_dna)
        return (baby)

    def saveAs(self, filename):
        self.image.save(filename)
