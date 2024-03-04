# Python code for node classes

import random

# 0       
class ZeroNode:
    def __init__(self, value=0):
        self.data = value

    def forward(self, value):
        self.data = value

# 1
class OneNode:
    def __init__(self, value=1):
        self.data = value

    def forward(self, value):
        self.data = value

# Inner
class InnerNode:
    def __init__(self, value=0):
        self.data = value

    def forward(self, value):
        self.data = value


# IntNode
class RandNode:
    def __init__(self, value=0):
        self.data = random.randint(0, 10) # random value between 0 and 10

    def forward(self, value):
        self.data = value

    
# Python code for a basic synapse class

class Synapse:
    def __init__(self, weight=1.0):
        self.weight = weight
        self.source = None
        self.target = None
            


# Python code for a basic synapse class

class Organism:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.synapses = []

    def new_brain(self):
        self.nodes.append(InnerNode())
        self.nodes.append(ZeroNode())
        self.nodes.append(OneNode())
        
        self.synapses.append(Synapse())
        self.synapses[-1].source = random.choice(self.nodes)
        self.synapses[-1].target = random.choice(self.nodes)


    def think(self):
        for synapse in self.synapses:
            synapse.target.forward(synapse.source.data)
            return synapse.target.data
        
    def child(self, partner):
        child = Organism()
        for i in range(len(self.synapses)):
            if random.random() > 0.5:
                child.synapses.append(self.synapses[i])
            else:
                child.synapses.append(partner.synapses[i])
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


print(world)