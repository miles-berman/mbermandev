class Synapse {
    constructor(weight = 1.0, source = null, target = null) {
        this.weight = weight;
        this.source = source;
        this.target = target;
    }

    cloneWithNewNodes(nodesMap) {
        // Create a new Synapse with the same weight, but source and target are looked up from the new nodesMap
        return new Synapse(this.weight, nodesMap.get(this.source), nodesMap.get(this.target));
    }
}

class RandNode {
    constructor() {
        this.data = Math.floor(Math.random() * 11);
        this.val = this.data;
    }

    forward() {
        this.data = this.val;
    }

    clone() {
        let clonedNode = new RandNode();
        clonedNode.data = this.data;
        clonedNode.val = this.val;
        return clonedNode;
    }
}

class InnerNode {
    constructor(value = 0) {
        this.data = value;
    }

    forward(value) {
        this.data = value;
    }

    clone() {
        return new InnerNode(this.data);
    }
}

class Organism {
    constructor() {
        this.nodes = [];
        this.synapses = [];
    }

    newBrain(size) {
        for (let i = 0; i < size; i++) {
            this.nodes.push(new RandNode());
            this.nodes.push(new InnerNode());
        }

        if (size > 0) {
            let synapse = new Synapse();
            synapse.source = this.nodes[Math.floor(Math.random() * this.nodes.length)];
            synapse.target = this.nodes[Math.floor(Math.random() * this.nodes.length)];
            this.synapses.push(synapse);
        }
    }

    think() {
        for (let synapse of this.synapses) {
            synapse.target.forward(synapse.source.data);
            return synapse.target.data;
        }
    }

    child(other) {
        let child = new Organism();
        let nodesMap = new Map();

        this.nodes.concat(other.nodes).forEach(node => {
            if (!nodesMap.has(node)) {
                nodesMap.set(node, node.clone());
            }
        });

        this.synapses.concat(other.synapses).forEach(synapse => {
            child.synapses.push(synapse.cloneWithNewNodes(nodesMap));
        });

        child.nodes = Array.from(nodesMap.values());

        return child;
    }
}

const size = [10, 10];
let world = [];
let target = 1;

function renderGrid() {
    const gridContainer = document.getElementById('grid');
    gridContainer.innerHTML = '';

    world.forEach(row => {
        row.forEach(organism => {
            let cell = document.createElement('div');
            let value = organism.think(); // Determine the value for visualization based on think method
            cell.className = 'cell ' + (value === target ? 'one' : 'zero');
            cell.textContent = value;
            gridContainer.appendChild(cell);
        });
    });
}

function generateGrid() {
    world = [];
    for (let i = 0; i < size[1]; i++) {
        world[i] = [];
        for (let j = 0; j < size[0]; j++) {
            let creature = new Organism();
            creature.newBrain(1);
            world[i][j] = creature;
        }
    }

    renderGrid();
}

function repopulate() {
    let newWorld = world.map(row => row.map(organism => {
        let creature = new Organism();
        creature.newBrain(1);
        return creature;
    }));

    world = newWorld;

    // Implement logic to determine winners and produce offspring
    // Note: This section needs logic adjustment according to your specific requirements
    let winners = [];
    for (let i = 0; i < size[1]; i++) {
        for (let j = 0; j < size[0]; j++) {
            if (world[i][j].think() === 1) {
                winners.push(world[i][j]);
            }
        }
    }

    let newGeneration = [];
    for (let i = 0; i < size[1]; i++) {
        newGeneration[i] = [];
        for (let j = 0; j < size[0]; j++) {
            newGeneration[i][j] = winners[Math.floor(Math.random() * winners.length)].child(winners[Math.floor(Math.random() * winners.length)]);
        }
    }

    world = newGeneration;
    

    renderGrid();
}

function naturalSelection() {
    repopulate();
}

window.onload = function() {
    generateGrid();
    setInterval(naturalSelection, 1000);
};
