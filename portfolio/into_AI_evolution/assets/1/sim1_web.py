

class Synapse:
    def __init__(self, weight=1.0):
        self.weight = weight
        self.source = None
        self.target = None

        
class ZeroNode:
    def __init__(self, value=0):
        self.data = value

    def forward(self, value):
        self.data = value

class OneNode:
    def __init__(self, value=1):
        self.data = value

    def forward(self, value):
        self.data = value

class InnerNode:
    def __init__(self, value=0):
        self.data = value

    def forward(self, value):
        self.data = value



class Organism:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.synapses = []

    def new_brain(self, size):
        for i in range(size):
            #self.nodes.append(InnerNode())
            self.nodes.append(ZeroNode())
            self.nodes.append(OneNode())

        self.synapses.append(Synapse())
        self.synapses[-1].source = random.choice(self.nodes)
        self.synapses[-1].target = random.choice(self.nodes)

    def think(self):
        for synapse in self.synapses:
            #synapse.target.forward(synapse.source.data * synapse.weight)
            synapse.target.forward(synapse.source.data)
            return synapse.target.data
    

from flask import Flask, render_template
import random

app = Flask(__name__)

# Your existing Python code here, with the Organism classes, etc.

@app.route('/')
def grid():
    size = (10, 10)  # 100 possible cells
    world = [[0 for x in range(size[0])] for y in range(size[1])]  # initialize world with 0s

    for i in range(10):
        for j in range(10):
            creature = Organism()
            creature.new_brain(1)
            val = creature.think()
            world[i][j] = val

    return render_template('grid.html', world=world)

if __name__ == '__main__':
    app.run(debug=True)