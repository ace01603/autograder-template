// Sample solution (delete from autograder)

var cat; // Should trigger no-var
let cat_w = 512; // Should trigger camelcase
let catH = 410;

async function setup() {
    cat = await loadImage("assets/pallas_cat.jpg");
    createCanvas(catW, catH);
    imageMode(CENTER);
}

function draw() {
    image(cat, width / 2, height / 2, cat_w, catH);
    if (catH < cat.height) {
        cat_w++;
        catH++;
    }
}

function inconsistentReturn(foo) { // should trigger consistent-return
    if (foo == 10) { // should trigger eqeqeq
        return true;
    }
}