# Python code for node classes

import random

# RandNode
class RandNode:
    def __init__(self, value=0):
        self.data = random.randint(0, 10) # random value between 0 and 10

    def forward(self, value):
        self.data = value

# Inner
class InnerNode:
    def __init__(self, value=0):
        self.data = value

    def forward(self, value):
        self.data = value


# Python code for a basic synapse class

class Synapse:
    def __init__(self, weight=1.0):
        self.weight = weight
        self.source = None
        self.target = None
            

# Python code for a basic organism class

class Organism:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.synapses = []

    def new_brain(self):
        self.nodes.append(InnerNode())
        self.nodes.append(RandNode())

        self.synapses.append(Synapse())
        self.synapses[-1].source = random.choice(self.nodes)
        self.synapses[-1].target = random.choice(self.nodes)


    def think(self):
        for synapse in self.synapses:
            synapse.target.forward(synapse.source.data)
            return synapse.target.data
        
    def mutate(self):
        for synapse in self.synapses:
            synapse.weight += random.uniform(-1, 1)
            synapse.source = random.choice(self.nodes)
            synapse.target = random.choice(self.nodes)

    def child(self, partner, mutation_rate=0.1):
        child = Organism()
        child.new_brain()
        for i in range(len(self.synapses)):
            rand = random.random()
            if rand > 0.5:
                child.synapses.append(self.synapses[i])
            else:
                child.synapses.append(partner.synapses[i])

            if rand <= mutation_rate:
                self.mutate()
                
        return child



# Python code for creating our grid

size = 10, 10 # 100 possible cells

world = [[0 for x in range(size[0])] for y in range(size[1])] # initialize world with 0s


for i in range(10):
    for j in range(10):
        creature = Organism()
        creature.new_brain()
        val = creature.think()
        world[i][j] = val

c = Organism()
c.new_brain
val = c.think()

d = Organism()
d.new_brain
val = d.think()

e = c.child(d)

print(e.think())
