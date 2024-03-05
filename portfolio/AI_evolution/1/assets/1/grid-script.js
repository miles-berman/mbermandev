class Synapse {
    constructor(weight = 1.0) {
        this.weight = weight;
        this.source = null;
        this.target = null;
    }
}

class ZeroNode {
    constructor(value = 0) {
        this.data = value;
    }

    forward(value) {
        this.data = value;
    }
}

class OneNode {
    constructor(value = 1) {
        this.data = value;
    }

    forward(value) {
        this.data = value;
    }
}

class InnerNode {
    constructor(value = 0) {
        this.data = value;
    }

    forward(value) {
        this.data = value;
    }
}

class Organism {
    constructor(nodes = []) {
        this.nodes = nodes;
        this.synapses = [];
    }

    newBrain(size) {
        for (let i = 0; i < size; i++) {
            this.nodes.push(new ZeroNode());
            this.nodes.push(new OneNode());
            this.nodes.push(new InnerNode());
        }

        let synapse = new Synapse();
        synapse.source = this.nodes[Math.floor(Math.random() * this.nodes.length)];
        synapse.target = this.nodes[Math.floor(Math.random() * this.nodes.length)];
        this.synapses.push(synapse);
    }

    think() {
        for (let synapse of this.synapses) {
            synapse.target.forward(synapse.source.data);
            return synapse.target.data;
        }
    }
}

const size = [10, 10]; // Grid size
let world = []; // Changed to let to allow reassignment

function generateGrid() {
    const gridContainer = document.getElementById('grid');
    gridContainer.innerHTML = ''; // Clear the existing grid
    
    world = []; // Reinitialize world array for each generation
    for (let i = 0; i < size[1]; i++) {
        world[i] = [];
        for (let j = 0; j < size[0]; j++) {
            let creature = new Organism();
            creature.newBrain(1);
            world[i][j] = creature.think();
        }
    }

    renderGrid(); // Call a new function to handle rendering
}

function renderGrid() {
    const gridContainer = document.getElementById('grid');
    gridContainer.innerHTML = ''; // Clear the existing grid
    
    world.forEach(row => {
        row.forEach(value => {
            let cell = document.createElement('div');
            cell.className = 'cell ' + (value === 1 ? 'one' : 'zero');
            cell.textContent = value;
            gridContainer.appendChild(cell);
        });
    });
}

function naturalSelection() {
    repopulate();
    renderGrid(); // Update the grid after changes
}



function repopulate() {
    for (let i = 0; i < world.length; i++) {
        for (let j = 0; j < world[i].length; j++) {
            if (world[i][j] === 0) {
                let creature = new Organism();
                creature.newBrain(1);
                world[i][j] = creature.think();
            }
        }
    }
}

// Call generateGrid on page load
window.onload = function() {
    generateGrid();
    setInterval(naturalSelection, 1000); // Periodically run naturalSelection every 1000ms
};
